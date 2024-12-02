import sys

import pyautogui
from PyQt5.QtWidgets import QApplication

from src.gui.window import MainWindow


def main():
    pyautogui.MINIMUM_DURATION = 0.0
    pyautogui.PAUSE = 0.0
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
