<p align="center"><img src="assets/icon.png" width="256" height="256" alt="EasyAutoClicker Logo"></p> <p align="center">Icon via Flaticon.com</p>

<h1 align="center">Easy Auto Clicker</h1> <h3 align="center">Easy Auto Clicker is an application for starting automatic clicking processes via a simple GUI. Each release can be found found <a href="https://github.com/CaymanFreeman/EasyAutoClicker/releases">here</a>.</h3>

## Settings

### Click Interval

##### Default: 100 Milliseconds
The click interval determines the amount of time between clicks. Setting this to 0 will attempt to click as fast as possible, possibly breaking any programs involved in responding to the click process. **Note:** Click interval accuracy begins to diminish with smaller intervals (~100ms to ~22ms depending on the system).

### Click Length

##### Default: 0
The click length determines how long to hold the click. For example, if the click length is set to 50 milliseconds, the mouse will be pressed down, wait for 50 milliseconds, then release. A click length of 0 will not perform a held click.

### Click Events

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

To build from source, a recipe for Windows and Linux can be found [here](https://github.com/CaymanFreeman/EasyAutoClicker/blob/main/.github/assets/build_recipes.md).
