#!/bin/bash
pyinstaller --noconfirm --onefile --name "easyautoclicker" --add-data="LICENSE.md:." --add-data="assets/icon.png:." src/app.py