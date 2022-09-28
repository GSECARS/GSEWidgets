#!/usr/bin/python3
# ----------------------------------------------------------------------
# GSEWidgets - Collection of gui widgets to be used in GSE software.
# Author: Christofanis Skordas (skordasc@uchicago.edu)
# Copyright (C) 2022  GSECARS, The University of Chicago, USA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from qtpy.QtCore import QSize
from qtpy.QtWidgets import QPushButton
from typing import Optional


class FlatButton(QPushButton):
    """Used to create instances of simple flat buttons"""

    def __init__(
            self,
            text: Optional[str] = None,
            size: Optional[QSize] = None,
            object_name: Optional[str] = "flat-button"
    ) -> None:
        super(FlatButton, self).__init__()

        self._text = text
        self._size = size
        self._object_name = object_name

        # Run configuration method
        self._configure_flat_button()

    def _configure_flat_button(self) -> None:
        """Basic configuration for the flat button."""
        # Set flat
        self.setFlat(True)

        # Add text
        if self._text is not None:
            self.setText(self._text)

        # Set the object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Set size
        if self._size is not None:
            self.setFixedSize(self._size)

        # Connect click event
        self.clicked.connect(self._button_click_event)

    def _button_click_event(self) -> None:
        """Clears the focus state of the button."""
        self.clearFocus()
