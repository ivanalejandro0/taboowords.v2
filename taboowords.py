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

import sys

try:
    from PySide import QtGui
except ImportError:
    print "PySide (Qt4 bindings for Python) is required for this application."
    sys.exit()

from wordsmodel import WordsModel
from ui.ui_taboowords import Ui_TabooWords


class TabooWords(QtGui.QMainWindow, object):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self._words_model = WordsModel('cards.db')

        self.ui = Ui_TabooWords()
        self.ui.setupUi(self)

        msj = "Se cargaron %s palabras." % self._words_model.contarPalabras()
        self.ui.statusbar.showMessage(msj)

        self._setup_connections()
        self._set_rules()

    def _setup_connections(self):
        self.ui.pbWin.clicked.connect(self._load_card)
        self.ui.pbSkip.clicked.connect(self._load_card)

        self.ui.pbTimerStart.clicked.connect(self.ui.lcdTimer.start)
        self.ui.pbTimerPause.clicked.connect(self.ui.lcdTimer.pause)
        self.ui.pbTimerReset.clicked.connect(self.ui.lcdTimer.reset)

    def _load_card(self):
        taboo_card = self._words_model.jugar()
        word = u'<u>Palabra:</u> <strong>{0}</strong><br><br>\n'
        card = word.format(taboo_card['palabra'])

        taboos = u'<u>Tabues:</u>\n<em><ul>\n'
        for taboo in taboo_card['tabues']:
            taboos += u'<li>{0}</li>\n'.format(taboo)
        taboos = taboos + '</ul></em>\n'

        html = u'<h3>{0}{1}</h3>'.format(card, taboos)

        self.ui.qteCard.setHtml(html)

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
    app = QtGui.QApplication(sys.argv)
    prog = TabooWords()
    prog.show()
    app.exec_()

    return 0


if __name__ == "__main__":
    main()
