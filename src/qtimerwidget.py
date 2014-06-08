#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Ivan Alejandro <ivanalejandro0@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import sys

try:
    from PySide import QtCore, QtGui
except ImportError:
    print "PySide (Qt4 bindings for Python) is required for this application."
    sys.exit()


class QTimerWidget(QtGui.QLCDNumber):
    out_of_time = QtCore.Signal()

    def __init__(self, parent=None):
        QtGui.QLCDNumber.__init__(self, parent)

        self.setNumDigits(3)
        self.setSegmentStyle(QtGui.QLCDNumber.Filled)

        self._timer = QtCore.QTimer()
        self._set_lcd_color()

        self._total_time = 60
        self._alert_time = 10

        self.display(self._total_time)
        self._timer.timeout.connect(self._decrement)

    def start(self):
        self._timer.start(1000)

    def pause(self):
        self._timer.stop()

    def reset(self):
        self._set_lcd_color()
        self.display(self._total_time)
        self._timer.stop()

    def _decrement(self):
        seconds = self.intValue()
        if seconds > 0:
            self.display(seconds - 1)
            if seconds == self._alert_time + 1:
                self._set_lcd_color(warning=True)
        else:
            self._timer.stop()
            self.out_of_time.emit()

    def _set_lcd_color(self, warning=False):
        color = QtCore.Qt.black
        if warning:
            color = QtCore.Qt.red

        self.setSegmentStyle(QtGui.QLCDNumber.Filled)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Foreground, color)
        self.setPalette(palette)
