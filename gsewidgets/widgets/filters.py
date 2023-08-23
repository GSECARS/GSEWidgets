#!/usr/bin/python3
# ----------------------------------------------------------------------
# GSEWidgets - Collection of gui widgets to be used in GSE software.
# Author: Christofanis Skordas (skordasc@uchicago.edu)
# Copyright (C) 2022-2023  GSECARS, The University of Chicago, USA
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
from urllib.parse import urlparse
from PyQt6.QtCore import QObject
from qtpy.QtCore import QObject, QEvent
from qtpy.QtWidgets import QLineEdit
from typing import Optional

__all__ = {"FileNameEventFilter", "FilePathEventFilter", "URIParseEventFilter", "IPv4EventFilter"}


class FileNameEventFilter(QObject):
    """Used to create file name focus out event filters to replace invalid characters with underscores."""

    def __init__(self, invalid_characters: Optional[str] = '<>"/\\|?*#&$: ') -> None:
        super(FileNameEventFilter, self).__init__()

        self._invalid_characters = invalid_characters

    def eventFilter(self, widget: QLineEdit, event: QEvent) -> bool:
        """Filter file name on focus out events."""
        if event.type() == QEvent.FocusOut:
            # Validate string
            text = widget.text()
            for character in self._invalid_characters:
                text = text.replace(character, "_")
            # Replace old text with the validated text
            widget.setText(text)

        return False


class FilePathEventFilter(FileNameEventFilter):
    """Used to create file path focus out event filters to replace invalid characters with underscores."""

    def __init__(self, invalid_characters: Optional[str] = '<>"|?*#&$: ') -> None:
        super(FilePathEventFilter, self).__init__(invalid_characters=invalid_characters)

    def eventFilter(self, widget: QLineEdit, event: QEvent) -> bool:
        """Filter file path on focus out events."""
        super(FilePathEventFilter, self).eventFilter(widget=widget, event=event)
        if event.type() == QEvent.FocusOut:
            text = widget.text()
            # Check/create file path
            file_path = Path(text)
            if not file_path.exists():
                file_path.mkdir(parents=True)
            # Replace the text with a PosixPath
            widget.setText(f"{file_path.as_posix()}/")
        return False


class URIParseEventFilter(QObject):
    """Used to parse URI on focus out events."""

    def __init__(self) -> None:
        super(URIParseEventFilter, self).__init__()

    def eventFilter(self, widget: QLineEdit, event: QEvent) -> bool:
        """Filter URI on focus out events."""
        if event.type() == QEvent.FocusOut:
            text = widget.text()

            # Parse URI
            parsed_uri = urlparse(text)
            # Check parsed uri
            if parsed_uri.scheme not in ["https", "http"]:
                # Clean the text of the URI input
                widget.setText("")
        return False


class IPv4EventFilter(QObject):
    """Used to parse IPv4 on focus out events."""

    def __init__(self, default_ip: Optional[str] = "127.0.0.1") -> None:
        super(IPv4EventFilter, self).__init__()

        self._default_ip = default_ip

    def eventFilter(self, widget: QLineEdit, event: QEvent) -> bool:
        """Filter IPv4 on focus out events."""
        if event.type() == QEvent.FocusOut:
            text = widget.text()

            # Check IPv4
            validated_ipv4 = self._valid_ip_check(ip=text)
            if not validated_ipv4:
                # Set the IP to the local host
                widget.setText(self._default_ip)
        return False

    def _valid_ip_check(self, ip: str) -> bool:
        """Check if the IPv4 address is valid."""
        sections = ip.split(".")

        # Check if the IP has 4 sections
        if len(sections) != 4:
            return False
        
        # Check if the IP is valid
        for section in sections:
            if not isinstance(int(section), int):
                return False
            
            if int(section) < 0 or int(section) > 255:
                return False
            
        return True
