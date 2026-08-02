#!/usr/bin/env python
"""
FOV boundary markers drawn on Steve's mosaic in response to "Draw FOV
Marker" messages from Dave (see storm_control/steve/tcpControl.py). These
are ephemeral, run-time-only annotations showing which FOVs have been
imaged in the current round, colored by whether a warning fired for that
FOV: not saved/loaded with .msc mosaic files, and not registered with
SteveItemsStore.addLoader() (unlike PositionItem).
"""
from PyQt5 import QtGui, QtWidgets

import storm_control.steve.coord as coord
import storm_control.steve.steveItems as steveItems


class FOVMarkerItem(steveItems.SteveItem):
    """
    A rectangle drawn around the boundary of one imaged FOV, yellow
    normally or warning_color if a warning fired for this FOV.
    """
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
    data_type = "fov_marker"
    normal_pen = QtGui.QPen(QtGui.QColor(255, 255, 0))
    warning_pen = QtGui.QPen(QtGui.QColor(255, 0, 0))

    def __init__(self, a_point = None, size_um = None, warning = False, **kwds):
        super().__init__(**kwds)

        self.x_size = coord.umToPix(size_um)
        self.y_size = coord.umToPix(size_um)

        self.graphics_item = QtWidgets.QGraphicsRectItem(0, 0, self.x_size, self.y_size)
        self.graphics_item.setPen(self.warning_pen if warning else self.normal_pen)
        self.graphics_item.setBrush(self.brush)

        # Above mosaic image tiles, below PositionItem (1000 deselected /
        # 2000 selected), so recorded positions always stay visible on top.
        self.graphics_item.setZValue(500.0)

        self.graphics_item.setPos(a_point.x_pix - 0.5 * self.x_size,
                                  a_point.y_pix - 0.5 * self.y_size)


#
# The MIT License
#
# Copyright (c) 2026 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
