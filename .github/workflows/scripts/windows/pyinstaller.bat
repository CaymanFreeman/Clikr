@echo off
pyinstaller --onefile --name EasyAutoClicker --add-data="LICENSE.md:." --add-data="assets\icon.png:." --windowed --icon=assets\icon.ico src\app.py