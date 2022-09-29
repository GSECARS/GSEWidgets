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
from qtpy.QtWidgets import QDoubleSpinBox, QAbstractSpinBox
from typing import Optional

__all__ = {
    "NumericSpinBox"
}


class NumericSpinBox(QDoubleSpinBox):
    """Used to create instances of numeric only spin boxes, without arrow buttons."""

    def __init__(
            self,
            min_value: float,
            max_value: float,
            default_value: float,
            incremental_step: float,
            precision: Optional[int] = 0,
            size: Optional[QSize] = None,
            object_name: Optional[str] = "numeric-spinbox"
    ) -> None:
        super(NumericSpinBox, self).__init__()

        self._min_value = min_value
        self._max_value = max_value
        self._default_value = default_value
        self._incremental_step = incremental_step
        self._precision = precision
        self._size = size
        self._object_name = object_name

        # Run configuration
        self._configure_numeric_spinbox()

    def _configure_numeric_spinbox(self) -> None:
        """Basic configuration for the numeric spinbox."""
        # Check for valid min and max
        if self._min_value >= self._max_value:
            raise ValueError("The min value must be lower than the max value.")
        else:
            # Set the min and max values
            self.setMinimum(self._min_value)
            self.setMaximum(self._max_value)

        # Check the default value
        if (
            self._default_value > self._max_value
            or self._default_value < self._min_value
        ):
            raise ValueError(
                "The default value must be within the range of the acceptable values for the spinbox."
            )
        # Set the default value
        self.setValue(self._default_value)

        # Check the incremental step
        if self._incremental_step > abs(self._max_value - self._min_value) / 3:
            raise ValueError(
                "The incremental step given must be maximum 1/3 of the total range of the spinbox."
            )
        # Set the incremental step
        self.setSingleStep(self._incremental_step)

        # Check the given precision
        if self._precision < 0:
            raise ValueError("Precision value can't be lesser than 0.")
        # Set the precision
        self.setDecimals(self._precision)

        # Set the object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Align to center
        self.setAlignment(Qt.AlignCenter)

        # Disable buttons
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)

        # Connect lineedit
        self.lineEdit().returnPressed.connect(self._return_pressed_event)

    def _return_pressed_event(self) -> None:
        """Clears the focus state of the spinbox."""
        self.clearFocus()
