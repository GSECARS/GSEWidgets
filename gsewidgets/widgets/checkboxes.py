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

from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QCheckBox
from typing import Optional

__all__ = {
    "CheckBox"
}


class CheckBox(QCheckBox):

    def __init__(
            self,
            text: Optional[str] = None,
            right_orientation: Optional[bool] = False,
            size: Optional[QSize] = None,
            object_name: Optional[str] = "simple-checkbox",
    ) -> None:
        super(CheckBox, self).__init__()

        self._text = text
        self._right_orientation = right_orientation
        self._size = size
        self._object_name = object_name

        # Run configuration
        self._configure_checkbox()

    def _configure_checkbox(self) -> None:
        """Basic configuration for the checkbox widget."""
        # Disable tristate
        self.setTristate(False)

        # Set text
        if self._text is not None:
            self.setText(self._text)

        # Set orientation
        if self._right_orientation:
            self.setLayoutDirection(Qt.RightToLeft)

        # Set the overall size
        if self._size is not None:
            self.setFixedSize(self._size)

        # Set the object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)
