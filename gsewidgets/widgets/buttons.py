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

from pathlib import Path
from qtpy.QtCore import QSize, QObject, Signal
from qtpy.QtWidgets import QPushButton, QFileDialog
from typing import Optional

__all__ = {
    "FlatButton",
    "FileBrowserButton",
    "DirectoryBrowserButton"
}


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


class AbstractBrowserButton(FlatButton):
    """Abstract button class to used for buttons that open QFileDialog widgets."""
    def __init__(
            self,
            text: Optional[str] = None,
            size: Optional[QSize] = None,
            object_name: Optional[str] = "flat-button",
            caption: Optional[str] = "Select File",
            invalid_characters: Optional[str] = '<>"\\|?*#& ',
    ) -> None:
        super(AbstractBrowserButton, self).__init__(
            text=text,
            size=size,
            object_name=object_name,
        )

        self._caption = caption
        self._invalid_characters = invalid_characters

        # Set the initial target directory
        self._target_directory = str(Path.home())

    @property
    def target_directory(self) -> str:
        return self._target_directory

    @target_directory.setter
    def target_directory(self, value: str) -> None:
        # Check invalid characters
        if self._invalid_characters is None:
            self._invalid_characters = '<>"\\|?*#& '
        # Validate based on invalid characters
        for char in self._invalid_characters:
            value = value.replace(char, "_")
        # Set the target directory
        self._target_directory = value


class FileBrowserButton(AbstractBrowserButton, QObject):
    """Used to create instances of flat button that open a QFileDialog to select a file."""
    file_path_changed: Signal = Signal(bool)

    def __init__(
            self,
            text: Optional[str] = None,
            size: Optional[QSize] = None,
            object_name: Optional[str] = "flat-button",
            caption: Optional[str] = "Select File",
            invalid_characters: Optional[str] = '<>"\\|?*#& ',
            file_extensions: list[str] = None,
    ) -> None:
        super(FileBrowserButton, self).__init__(
            text=text,
            size=size,
            object_name=object_name,
            caption=caption,
            invalid_characters=invalid_characters,
        )

        self._file_extensions = file_extensions

        self._file_path: str = ""
        self._filter: str = ""

        # Configure the file filter string
        self._configure_file_filter()

    def _configure_file_filter(self) -> None:
        """Sets the value of the filter string for the accepted files."""
        if self._file_extensions is None:
            # Keep filter open to all files
            self._filter = "All files (*)"
        else:
            for extension in self._file_extensions:
                # Make sure that the extension starts with *.
                if not extension.startswith("*."):
                    extension = f"*.{extension}"
                # Add extensions to the filter string
                self._filter += f" {extension}"

            # Remove first character
            self._filter = self._filter[1:]

    def _button_click_event(self) -> None:
        """Uses QFileDialog to get the selected file path, and emits a file_path_changed signal."""
        # Clears the focus state of the button
        self.clearFocus()
        # Create the QFileDialog widget
        dialog = QFileDialog()
        # Set the file mode
        dialog.setFileMode(QFileDialog.ExistingFile)
        # Get options
        options = QFileDialog.Options()
        # Get the new path for the file
        new_file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption=self._caption,
            directory=self._target_directory,
            filter=self._filter,
            options=options,
        )

        # Update the file path and emit the file_path_changed signal
        if new_file_path != "":
            self._file_path = new_file_path
            self.file_path_changed.emit(True)

    @property
    def file_path(self) -> str:
        return self._file_path


class DirectoryBrowserButton(AbstractBrowserButton, QObject):
    """Used to create instances of flat button that open a QFileDialog to select a directory."""
    directory_changed: Signal = Signal(bool)

    def __init__(
            self,
            text: Optional[str] = None,
            size: Optional[QSize] = None,
            object_name: Optional[str] = "flat-button",
            caption: Optional[str] = "Select File",
            invalid_characters: Optional[str] = '<>"\\|?*#& ',
    ) -> None:
        super(DirectoryBrowserButton, self).__init__(
            text=text,
            size=size,
            object_name=object_name,
            caption=caption,
            invalid_characters=invalid_characters,
        )

        self._directory = ""

    def _button_click_event(self) -> None:
        """Uses QFileDialog to get the selected directory, and emits a directory_changed signal."""
        # Clears the focus state of the button
        self.clearFocus()
        # Open file dialog and get the directory
        new_directory = QFileDialog.getExistingDirectory(
            parent=self,
            caption=self.caption,
            directory=self.target_directory
        )
        # Update the directory path and emit the directory_changed signal
        if new_directory != "":
            self._directory = new_directory
            self.directory_changed.emit(True)

    @property
    def directory(self) -> str:
        return self._directory
