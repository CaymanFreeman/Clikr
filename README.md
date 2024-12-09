<p align="center">
  <img src="assets/icon.png" width="256" height="256" alt="EasyAutoClicker Logo">
</p>

<div id="toc" align="center">
  <ul style="list-style: none;">
    <summary>
      <h1 align="center">
        Easy Auto Clicker
      </h1>
    </summary>
  </ul>
</div>

<h3 align="center">
  Starting automatic clicking processes via a simple GUI.
</h3>

<p align="center">
  <a href="https://github.com/CaymanFreeman/EasyAutoClicker/blob/main/LICENSE.md"><img alt="MIT License" src="https://img.shields.io/github/license/CaymanFreeman/EasyAutoClicker?style=flat&color=%23B20D35"></a>&nbsp;
  <a href="https://www.python.org/"><img alt="Built With Python" src="https://img.shields.io/badge/built_with-Python-brightgreen&style=flat"></a>&nbsp;
  <a href="https://github.com/CaymanFreeman/EasyAutoClicker/releases"><img alt="Release" src="https://img.shields.io/github/v/release/CaymanFreeman/EasyAutoClicker?include_prereleases&display_name=release&style=flat&color=%239d69c3"></a>&nbsp;
  <a href="https://www.linkedin.com/in/caymanfreeman/"><img alt="linkedin" src="https://img.shields.io/badge/linkedin-Connect_with_me-%230072b1?style=flat"></a>
</p>

## Releases

Each release can be found found <a href="https://github.com/CaymanFreeman/EasyAutoClicker/releases">here</a>.

## Settings

If any fields are left empty, the default value will be used.

### Interval

##### Default: 100 Milliseconds
The click interval determines the amount of time between clicks. Setting this to 0 will attempt to click as fast as possible, possibly breaking any programs involved in responding to the click process. **Note:** Click interval accuracy begins to diminish with smaller intervals (~100ms to ~22ms depending on the system).

### Length

##### Default: 0
The click length determines how long to hold the click. For example, if the click length is set to 50 milliseconds, the mouse will be pressed down, wait for 50 milliseconds, then release. A click length of 0 will not perform a held click.

### Event Count

##### Default: Infinite
The click events determine how many times to cause a click event. For example, if this is set to 5, the process will conduct 5 different click events then end automatically.

### Clicks Per Event

##### Default: 1
The clicks per event determine how many times to click each time a click event occurs. For example, setting this to 2 will cause each event to be a double click, 3 to be a triple click, etc. This setting is incompatible with a click length greater than 0.

### Mouse Button

##### Default: Left (M1)
The mouse button determines which button on the mouse will be used for each click event.

### Location

##### Default: None
The location determines where each click event will occur. A location can be picked by pressing the "Change" button and clicking the desired location on the screen. The location can be reset to "None" by clicking the "Change" button and pressing Esc. If a location is not specified, the user-controlled mouse position will be used instead. If using a specific location, a hotkey must be set as well to prevent softlocking.

### Hotkey

The hotkey sequence determines which keys will toggle the click process. To change the hotkey, click into the field and begin typing. Click out of the field to stop editing the sequence or press Esc to clear it. A hotkey must be set if a specific location is provided.

## Build From Source

### Requirements

Both recipes assume you have [git](https://git-scm.com/downloads) and [python3](https://www.python.org/downloads) installed.

## Windows

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

## Linux

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
