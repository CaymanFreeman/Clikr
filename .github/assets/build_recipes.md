# Requirements

Both recipes assume you have [git](https://git-scm.com/downloads) and [python3](https://www.python.org/downloads) installed.

# Windows

### Clone Repository
```batch
git clone https://github.com/CaymanFreeman/EasyAutoClicker && cd EasyAutoClicker
```

### Virtual Environment Setup
```batch
python -m venv .venv
.venv\Scripts\activate.bat
```

### Install Dependencies
```batch
python -m pip install --upgrade pip
pip install -r ./requirements.txt
pip install pyinstaller
```

### PyInstaller Build
```batch
pyinstaller --noconfirm --onefile --name "EasyAutoClicker" --windowed --add-data="LICENSE.md:." --icon="assets\icon.ico" --add-data="assets\icon.png:." src\app.py
```

### Run Executable

The executable will be located at `dist/EasyAutoClicker.exe`.

# Linux

### Clone Repository
```bash
git clone https://github.com/CaymanFreeman/EasyAutoClicker && cd EasyAutoClicker
```

### Virtual Environment Setup
```bash
python -m venv .venv
.venv/bin/activate
```

### Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r ./requirements.txt
pip install pyinstaller
```

### PyInstaller Build
```bash
pyinstaller --noconfirm --onefile --name "easyautoclicker" --add-data="LICENSE.md:." --add-data="assets/icon.png:." src/app.py
```

### Run Binary

The binary will be located at `dist/easyautoclicker`.