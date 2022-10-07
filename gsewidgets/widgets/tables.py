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

from qtpy.QtCore import QObject, Signal, Qt
from qtpy.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView, QCheckBox, QTableWidgetItem
from typing import Optional

from gsewidgets import NoWheelNumericSpinBox, NumericDataSpinBoxModel

__all__ = {
    "XYZCollectionPointsTable"
}


class TableWidget(QTableWidget):
    """Used to create instances of simple table templates."""

    def __init__(
            self,
            columns: Optional[int] = None,
            rows: Optional[int] = None,
            horizontal_headers: Optional[list[str]] = None,
            column_stretch: Optional[int] = None,
            object_name: Optional[str] = None
    ) -> None:
        super(TableWidget, self).__init__()

        self._columns = columns
        self._rows = rows
        self._horizontal_headers = horizontal_headers
        self._column_stretch = column_stretch
        self._object_name = object_name

        self._configure_table_widget()

    def _configure_table_widget(self) -> None:
        """Basic configuration of the table widget."""
        # Set the columns
        if self._columns is not None:
            if self._columns >= 1:
                self.setColumnCount(self._columns)

        # Set the rows
        if self._rows is not None:
            if self._rows >= 1:
                self.setRowCount(self._rows)

        # Set horizontal headers
        if self._horizontal_headers is not None:
            self.setHorizontalHeaderLabels(self._horizontal_headers)
            self.horizontalHeader().setVisible(True)
        else:
            self.horizontalHeader().setVisible(False)

        # Set column stretch
        if self._column_stretch is not None:
            if 0 <= self._column_stretch <= self._columns - 1:
                self.horizontalHeader().setSectionResizeMode(
                    self._column_stretch, QHeaderView.Stretch
                )
        # Set object name
        if self._object_name is not None:
            self.setObjectName(self._object_name)

        # Hide vertical header
        self.verticalHeader().setVisible(False)
        # Disable grid
        self.setShowGrid(False)
        # Disable header buttons
        self.horizontalHeader().setDisabled(True)
        # Set alternating row colors
        self.setAlternatingRowColors(True)
        # Set selection behavior and mode
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def delete_selection(self) -> None:
        """Removes the selected row from the table."""
        # Get the row index
        row_index = self.currentRow()
        # Remove the row
        if row_index >= 0:
            self.removeRow(row_index)

    def clear_table(self) -> None:
        """Removes all the existing rows from the table, excluding the headers."""
        # Get the total rows
        row_count = self.rowCount()
        # Remove the rows
        for row in range(row_count):
            self.removeRow(row)
        # Reset the row count
        self.setRowCount(0)


class XYZCollectionPointsTable(TableWidget, QObject):
    """Used to create instances of simple XYZ Collection Points table."""
    enabled_checkboxes_updated: Signal = Signal()

    def __init__(
            self,
            columns: Optional[int] = 5,
            rows: Optional[int] = 0,
            horizontal_headers=None,
            column_stretch: Optional[int] = 0,
            object_name: Optional[str] = "xyz-table"
    ) -> None:
        # Check mutable input
        if horizontal_headers is None:
            horizontal_headers = ["Name", "X", "Y", "Z", "Enabled"]
        # Initialize
        super(XYZCollectionPointsTable, self).__init__(
            columns=columns,
            rows=rows,
            horizontal_headers=horizontal_headers,
            column_stretch=column_stretch,
            object_name=object_name
        )

        self._enabled_checkboxes: list[QCheckBox] = []
        self._numeric_data_list: list[list[NumericDataSpinBoxModel]] = []
        self._row_counter: int = 0

    def _available_name_check(self) -> None:
        """Checks for the next available point name."""
        self._row_counter = 0
        for row in range(self.rowCount() - 1):
            self._row_counter += 1

            if not f"point{self._row_counter}" == self.item(row, 0).text():
                return None

    def add_point(
            self,
            x: NumericDataSpinBoxModel,
            y: NumericDataSpinBoxModel,
            z: NumericDataSpinBoxModel,
    ) -> None:
        """Adds a single collection point to the bottom of the list."""
        # Get rows
        row = self.rowCount()
        # Increase the row count by 1
        self._row_counter = row + 1
        self.setRowCount(self._row_counter)

        # Create the next name based on the row counter
        dynamically_created_name = f"point{self._row_counter}"
        # Check if the name already exists
        if row > 0:
            for existing_row in range(row):
                if dynamically_created_name == self.item(existing_row, 0).text():
                    temp_row_counter = self._row_counter
                    self._available_name_check()
                    dynamically_created_name = f"point{self._row_counter}"
                    self._row_counter = temp_row_counter
        # Create the name widget
        name_widget = QTableWidgetItem(dynamically_created_name)
        name_widget.setTextAlignment(Qt.AlignCenter)
        # Set the item
        self.setItem(row, 0, name_widget)

        # Create the X,Y and Z widgets
        # X widget
        x_widget = NoWheelNumericSpinBox(
            min_value=x.min_value,
            max_value=x.max_value,
            default_value=x.current_value,
            incremental_step=x.incremental_step,
            precision=x.precision
        )
        x_widget.valueChanged.connect(lambda: x.spinbox_value_changed.emit(x_widget.value()))
        self.setCellWidget(row, 1, x_widget)
        # Y widget
        y_widget = NoWheelNumericSpinBox(
            min_value=y.min_value,
            max_value=y.max_value,
            default_value=y.current_value,
            incremental_step=y.incremental_step,
            precision=y.precision
        )
        y_widget.valueChanged.connect(lambda: y.spinbox_value_changed.emit(y_widget.value()))
        self.setCellWidget(row, 2, y_widget)
        # Z widget
        z_widget = NoWheelNumericSpinBox(
            min_value=z.min_value,
            max_value=z.max_value,
            default_value=z.current_value,
            incremental_step=z.incremental_step,
            precision=z.precision
        )
        z_widget.valueChanged.connect(lambda: z.spinbox_value_changed.emit(z_widget.value()))
        self.setCellWidget(row, 3, z_widget)
        # Append to the numeric list
        self.numeric_data_list.append([x, y, z])

        # Create the enabled checkbox
        checkbox = QCheckBox()
        # Set default state as checked
        checkbox.setChecked(True)
        # Add to table
        self.setCellWidget(row, 4, checkbox)
        # Add to the enabled checkboxes list
        self.enabled_checkboxes.append(checkbox)
        # Connect checkbox state changed
        checkbox.stateChanged.connect(lambda: self.enabled_checkboxes_updated.emit())

    def enable_all_points(self) -> None:
        """Sets the check state for all the checkboxes included in the list of checkboxes."""
        for checkbox in self.enabled_checkboxes:
            checkbox.setChecked(True)

    def clear_table(self) -> None:
        """Deletes all the rows of the table and clears the list of checkboxes."""
        # Remove existing rows
        super(XYZCollectionPointsTable, self).clear_table()
        # Clear the list of checkboxes
        self._enabled_checkboxes.clear()

    def delete_selection(self) -> None:
        """Removes the selected row from the table and the checkbox entry from the list of checkboxes."""
        index = self.currentRow()
        if index >= 0:
            self.removeRow(index)
            self.enabled_checkboxes.pop(index)
            self.numeric_data_list.pop(index)

    @property
    def enabled_checkboxes(self) -> list[QCheckBox]:
        return self._enabled_checkboxes

    @property
    def numeric_data_list(self) -> list[list[NumericDataSpinBoxModel]]:
        return self._numeric_data_list
