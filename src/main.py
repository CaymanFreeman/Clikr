# Copyright (C) 2025  Cayman Freeman
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Entry point for launching Clikr."""

import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.ui.window import Window

LOG_FORMAT: str = "%(asctime)s %(levelname)s %(message)s"
DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def _setup_logging() -> None:
    """Configures the logging with the provided formats."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATETIME_FORMAT)


def main() -> None:
    """Initializes logging and launches the PyQt window."""
    _setup_logging()

    app: QApplication = QApplication(sys.argv)
    _window: Window = Window()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
