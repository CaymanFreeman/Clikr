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
