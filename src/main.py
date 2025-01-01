import logging

import sys

from PyQt6.QtWidgets import QApplication

from src.ui.window import Window

LOG_FORMAT: str = "%(asctime)s %(levelname)s %(message)s"
DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATETIME_FORMAT,
    )


def main():
    setup_logging()

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
