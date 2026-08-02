#!/usr/bin/env python
"""
Handles remote control of Steve (via TCP/IP), for Dave to report FOV
markers as movies complete and to clear them at round boundaries. This is
a listening server, mirroring storm_control/hal4000/tcpControl/tcpControl.py,
but much simpler: Steve has no message queue / module chain to route
through, so each message is handled synchronously and replied to
immediately (unlike Hal's TCPControl, there is no multi-step "action"
that waits on further internal messages).

Hazen's Steve<->Hal comm.py is the client side of an analogous connection;
this is the server side of the new, separate Dave<->Steve connection.
"""
from PyQt5 import QtCore

import storm_control.steve.coord as coord
import storm_control.steve.fovMarker as fovMarker


class Controller(QtCore.QObject):
    """
    The interface between Steve and a TCP client (Dave). Handles two
    message types:

    "Draw FOV Marker" - data: stage_x, stage_y (microns), warning (bool).
    "Clear FOV Markers" - data: none.

    Anything else gets an error response, same as an unhandled TCP
    message elsewhere in storm-control.
    """
    def __init__(self, item_store = None, fov_size_um = None, server = None, verbose = True, **kwds):
        super().__init__(**kwds)
        self.fov_size_um = fov_size_um
        self.item_store = item_store
        self.server = server
        self.verbose = verbose

        self.server.messageReceived.connect(self.handleMessageReceived)

    def cleanUp(self):
        self.server.close()

    def handleMessageReceived(self, message):
        if self.verbose:
            print(">TCP message received (Steve):")
            print(message)
            print("")

        if message.isType("Draw FOV Marker"):
            a_point = coord.Point(message.getData("stage_x"),
                                  message.getData("stage_y"),
                                  "um")
            marker = fovMarker.FOVMarkerItem(a_point = a_point,
                                             size_um = self.fov_size_um,
                                             warning = message.getData("warning", False))
            self.item_store.addItem(marker)

        elif message.isType("Clear FOV Markers"):
            self.item_store.removeItemType(fovMarker.FOVMarkerItem)

        else:
            message.setError(True, "Unknown message type '" + message.getType() + "'")

        self.server.sendMessage(message)


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
