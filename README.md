# Readme
The code provided in this repository represents the software for the prototype of the smart home warning system described in "Getting the Residents' Attention: The Perception of Warning Channels in Smart Home Warning Systems."

## Hardware of the prototype:
The prototype runs on a Raspberry Pi 4 using Raspberry Pi OS, a debian-based operating system. Several components are connected to the Pi:
- 5-inch touch display with a resolution of 800x480
- USB speaker
- GSM hat
- ZigBee 3.0 USB dongle

## Autostart
To ensure the code runs as soon as the Raspberry Pi boots, the main_dialog.py file needs to be added to the autostart. This can be done by executing the following steps:
1. Open the terminal and create a .desktop file in the autostart directory
2. Add the following line to the .desktop file:  `[Desktop Entry] python3.9 /home/pi/masterthesis/main_dialog.py`
3. Save the file and reboot the Pi afterwardsf

## Files
The log files created by the application can be found at /home/pi/masterthesis/resources/log.log. The evaluation of the user is stored at /home/pi/masterthesis/resources/feedback. The paths can be configured by changing the corresponding variables in the class util.py.
