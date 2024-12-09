#!/bin/bash
pyinstaller --noconfirm --onefile --name "easyautoclicker" --add-data="LICENSE.md:." --hidden-import pynput.keyboard._xorg --hidden-import pynput.mouse._xorg src/app.py