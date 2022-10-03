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

from qtpy.QtWidgets import QFrame
from typing import Optional

__all__ = {
    "VerticalLine"
}


class Line(QFrame):

    def __init__(self, object_name: Optional[str] = None) -> None:
        super(Line, self).__init__()

        # Set the object name
        if object_name is not None:
            self.setObjectName(object_name)


class VerticalLine(Line):
    """Used to created vertical lines."""
    def __init__(self, object_name: Optional[str] = "vertical-line") -> None:
        super(VerticalLine, self).__init__(object_name=object_name)

        # Set vertical orientation
        self.setFrameShape(QFrame.Shape.VLine)
