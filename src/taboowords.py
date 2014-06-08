#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Ivan Alejandro <ivanalejandro0@gmail.com>
#
# This file is part of TabooWords.
#
# TabooWords is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TabooWords is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TabooWords.  If not, see <http://www.gnu.org/licenses/>.

import signal
import sys

from PySide import QtCore, QtGui

from wordsmodel import WordsModel
from ui.ui_taboowords import Ui_TabooWords


class TabooWords(QtGui.QMainWindow, object):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.ui = Ui_TabooWords()
        self.ui.setupUi(self)

        self._words_model = WordsModel('cards.db')

        msj = "Se cargaron %s palabras." % self._words_model.contarPalabras()
        self.ui.statusbar.showMessage(msj)

        self._current_card = None
        self._cards_remaining = 0
        self._cards_win = 0
        self._cards_lose = 0

        self._score_A = 0
        self._score_B = 0

        self._setup_connections()
        self._set_rules()

    def _setup_connections(self):
        # implicit connections:
        # self.ui.pbWin.clicked.connect(self._load_card)
        # self.ui.pbSkip.clicked.connect(self._load_card)
        self.ui.pbNewCardsRound.clicked.connect(self._on_new_round)

        self.ui.pbTimerStart.clicked.connect(self.ui.lcdTimer.start)
        self.ui.pbTimerPause.clicked.connect(self.ui.lcdTimer.pause)
        self.ui.pbTimerReset.clicked.connect(self.ui.lcdTimer.reset)

        self.ui.lcdTimer.out_of_time.connect(self._out_of_time)

    def _out_of_time(self):
        self.ui.pbWin.setEnabled(False)
        self.ui.pbSkip.setEnabled(False)
        self.ui.qteCard.setHtml("<strong>El tiempo se ha terminado.</strong>")

    def _load_card(self):
        taboo_card = self._words_model.jugar()
        self._current_card = taboo_card

        word = u'<u>Palabra:</u> <strong>{0}</strong><br><br>\n'
        card = word.format(taboo_card['palabra'])

        taboos = u'<u>Tabues:</u>\n<em><ul>\n'
        for taboo in taboo_card['tabues']:
            taboos += u'<li>{0}</li>\n'.format(taboo)
        taboos = taboos + '</ul></em>\n'

        html = u'<h3>{0}{1}</h3>'.format(card, taboos)

        self.ui.qteCard.setHtml(html)
        self._update_remaining_cards()

    def _update_remaining_cards(self):
        if self._cards_remaining > 0:
            self._cards_remaining -= 1
            self.ui.lcdRemainingCards.display(self._cards_remaining)
        else:
            self.ui.pbWin.setEnabled(False)
            self.ui.pbSkip.setEnabled(False)
            self.ui.qteCard.setHtml("<strong>Fin de la partida.</strong>")

    @QtCore.Slot()
    def on_pbWin_clicked(self):
        self._cards_win += 1
        word = self._current_card
        if word is not None:
            item = QtGui.QTableWidgetItem(word['palabra'])
            details = 'Tabues: '+', '.join(word['tabues'])
            item.setToolTip(details)
            self.ui.twGuessedCards.setItem(self._cards_win-1, 0, item)

        cards = int(self.ui.leGuessedCards.text())
        cards += 1
        self.ui.leGuessedCards.setText(str(cards))
        self._load_card()

    @QtCore.Slot()
    def on_pbSkip_clicked(self):
        self._cards_lose += 1
        word = self._current_card
        if word is not None:
            item = QtGui.QTableWidgetItem(word['palabra'])
            details = 'Tabues: '+', '.join(word['tabues'])
            item.setToolTip(details)
            self.ui.twSkippedCards.setItem(self._cards_lose-1, 0, item)

        cards = int(self.ui.leSkippedCards.text())
        cards += 1
        self.ui.leSkippedCards.setText(str(cards))
        self._load_card()

    @QtCore.Slot()
    def _on_new_round(self):
        # reset game status
        self._cards_remaining = 5
        self.ui.lcdRemainingCards.display(self._cards_remaining)

        # clear win/skip tables:
        for row in xrange(5):
            self.ui.twSkippedCards.setItem(row, 0, QtGui.QTableWidgetItem(''))
            self.ui.twGuessedCards.setItem(row, 0, QtGui.QTableWidgetItem(''))

        self._current_card = None
        self._cards_win = 0
        self._cards_lose = 0

        self.ui.leSkippedCards.setText('0')
        self.ui.leGuessedCards.setText('0')

        self.ui.pbWin.setEnabled(True)
        self.ui.pbSkip.setEnabled(True)
        self.ui.pbProcessRound.setEnabled(True)

        self._load_card()

    @QtCore.Slot()
    def on_pbProcessRound_clicked(self):
        if self.ui.rbPlayingA.isChecked():
            self._score_A += self._cards_win
            self.ui.lcdScoreTeamA.display(self._score_A)
        else:
            self._score_B += self._cards_win
            self.ui.lcdScoreTeamB.display(self._score_B)

        self.ui.pbProcessRound.setEnabled(False)

    def _set_rules(self):
        # TODO: load rules from file
        self._rules = ""
        msj = self.tr("Para instrucciones debe ir al menu\nAyuda->Como jugar?")
        self.ui.qteCard.setHtml(msj)

    def _show_instructions(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(self._rules)
        msgBox.exec_()

    def _show_about(self):
        msgBox = QtGui.QMessageBox()
        self.about = (
            "<center><strong>TabooWords</strong</center><br />\n"
            "Versi&oacute;n inform&aacute;tica del juego de tablero en grupos"
            "en el cual se debe explicar una palabra a tus compa&ntilde;eros"
            "sin usar las palabras dadas como taboo.<br /><br />\n"
            "Autor: Ivan Alejandro &lt;ivanalejandro0@gmail.com&gt;"
        )
        msgBox.setText(self.about)
        msgBox.exec_()


def main():
    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtGui.QApplication(sys.argv)
    prog = TabooWords()
    prog.show()
    app.exec_()

    return 0


if __name__ == "__main__":
    main()
