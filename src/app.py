import logging
import multiprocessing
import sys

from PyQt5.QtWidgets import QApplication

from window_logic import AppWindow


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
    window = AppWindow(logger)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        multiprocessing.freeze_support()
    main()
