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

from qtpy.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView
from typing import Optional


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
