#!/bin/bash
pyinstaller --noconfirm --onefile --name EasyAutoClicker --add-data="LICENSE.md:." --add-data="assets/icon.png:." src/app.py