<p align="center"><img src="assets/icon.png" width="256" height="256" alt="Easy Auto Clicker Logo"></p> <p align="center">Icon via Flaticon.com</p>

<h1 align="center">Easy Auto Clicker</h1> <h3 align="center">Easy Auto Clicker is an application for starting automatic clicking processes via a simple GUI. A Windows installer and source code is included with each release found <a href="https://github.com/CaymanFreeman/EasyAutoClicker/releases">here</a>.</h3>

## Settings

### Click Length

##### Default: 0
The click length determines how long to hold the click. For example, if the click length is set to 50 milliseconds, the mouse will be pressed down, wait for 50 milliseconds, then release. A click length of 0 will not perform a held click. Setting this to any value greater than 0 will assume the clicks per event to be 0. Setting this value greater than the click interval will cause the mouse to be pressed down constantly but will still register a click at the click interval.

### Click Interval

##### Default: 100 Milliseconds
The click interval determines the amount of time between clicks. Setting this to 0 will attempt to click as fast as possible, possibly breaking any programs involved in responding to the click process. **Note:** Click interval accuracy begins to diminish with smaller intervals (~22ms in testing).

### Mouse Button

##### Default: Left (M1)
The mouse button determines which button on the mouse will be used for each click event.

### Clicks Per Event

##### Default: 1
The clicks per event determine how many times to click each time a click event occurs. For example, setting this to 2 will cause each event to be a double click, 3 to be a triple click, etc. This setting is incompatible with a click length greater than 0.

### Click Events

##### Default: 0
The click events determine how many times to cause a click event. For example, if this is set to 5, the process will conduct 5 different click events then end automatically. Setting this to 0 will cause the click process to send click events indefinitely (until manually stopped via hotkey or the stop button).

### Location

##### Default: Current Cursor Location
The location determines where each click event will occur. A location can be picked by pressing the "Pick Location" button and clicking the desired location on the screen. The location can be reset to the current cursor location by clicking the "Pick Location" button and pressing Escape.

### Hotkey

##### Default: CTRL+F8
The hotkey sequence determines which keys will toggle the click process. To change the hotkey, press the "Change Hotkey" button, enter the desired hotkey (up to 3 keys), and press "Click to Confirm".

## Build Information

Clone:

```
git clone https://github.com/CaymanFreeman/EasyAutoClicker.git
cd EasyAutoClicker
```

Required Packages:

```
pip install pyinstaller customtkinter pyautogui keyboard mouse
```

Build (Windows):

```
$ctk_path = pip show customtkinter | Select-String -Pattern "Location: (.*)" | ForEach-Object { $_.Matches.Groups[1].Value }
pyinstaller --noconfirm --name "EasyAutoClicker" --icon="assets\icon.ico" --onedir --windowed --add-data "$ctk_path\customtkinter;customtkinter" app.py
xcopy "assets" "dist\EasyAutoClicker\assets\" /E /I /Y
```

Build (Linux):

```
ctk_path=$(pip show customtkinter | grep 'Location:' | awk '{print $2}')
pyinstaller --noconfirm --name "EasyAutoClicker" --icon="assets/icon.ico" --onedir --windowed --add-data "$ctk_path/customtkinter;customtkinter" app.py
cp -ruv "assets" "dist/EasyAutoClicker/assets/"
```
