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

from qtpy.QtCore import QSize, Qt
from qtpy.QtWidgets import QLineEdit
from typing import Optional

__all__ = {
    "InputBox",
}


class InputBox(QLineEdit):
    """Used to create instances of simple input boxes."""

    def __init__(
        self,
        placeholder: Optional[str] = None,
        size: Optional[QSize] = None,
        object_name: Optional[str] = "input-box"
    ) -> None:
        super(InputBox, self).__init__()

        self._placeholder = placeholder
        self._size = size
        self._object_name = object_name

        # Run configuration method
        self._configure_input_box()

    def _configure_input_box(self) -> None:
        """Basic configuration of the simple input box."""
        # Set placeholder text
        if self._placeholder is not None:
            self.setPlaceholderText(self._placeholder)

        # Set size
        if self._size is not None:
            self.setFixedSize(self._size)

        # Set object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Center align
        self.setAlignment(Qt.AlignCenter)

        # Connect the return pressed event
        self.returnPressed.connect(self._return_pressed_event)

    def _return_pressed_event(self) -> None:
        """Clears the focus state."""
        self.clearFocus()
