# Pyclops
Pyclops is a simple screen-recording utility. It can be configured to record any portion of the screen and works on multi-monitor setups. It may be set to record only screen captures containing changes within the recording area. Although it is far from optimized, pyclops can record 4K captures at ~30 frames per second.

## Installation
Install the required python utilities,
- PySimpleGUI
- Pillow
- mss

clone this library, and run in your Python interpeter of choice.

## Usage
Run the python script. Use the GUI to set up the desired capture area/interval. Click the start button to initiate the capture process. 

![Droste effect](https://github.com/steubengineer/pyclops/blob/main/example.png)

Screen capture files will be saved to the user home directory, or the user-specified directory. Saved filenames will have the format YYYY_MM_DD_HHMM_ms.png. The year, month, day, hour, and minute correspond to the time at which the user clicked 'start.' The ms suffix denotes the number of milliseconds elapsed since the start time at which the corresponding capture was taken. 