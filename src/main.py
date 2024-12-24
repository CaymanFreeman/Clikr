import logging

import sys

from PyQt6.QtWidgets import QApplication

from window import Window


def log_setup() -> logging.Logger:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


def main():
    logger = log_setup()
    app = QApplication(sys.argv)
    window = Window(logger)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
