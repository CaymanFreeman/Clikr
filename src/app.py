import multiprocessing
import sys

from PyQt5.QtWidgets import QApplication

from window_logic import AppWindow


def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        multiprocessing.freeze_support()
    main()
