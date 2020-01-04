# ArduinoFortune

Display a fortune on an LCD.

Tapping the screen will change the fortune.

## Hardware needed:
+ Arduino Uno
+ 2.8 in TFT LCD

Both are available from [Banggood](https://www.banggood.com/Geekcreit-UNO-R3-Improved-Version-2_8TFT-LCD-Touch-Screen-2_4TFT-Touch-Screen-Display-Module-Kit-p-1428291.html) for cheap.

## Overview

The splitFortunes.py program takes the Linux Fortune files and splits each fortune into a single file, grouping files in subdirectories of 255 files each.  This is done to increase the speed of the fortune displaying.

I tried reading the Linux fortune files, but if a large fortune file was chosen and a fortune near the end of that file was chosen, it would take upwards of 8 seconds for the fortune to display.  A co-worker suggested the single-fortune-in-a-file solution which greatly improved things, but the SD card library goes through the directory sequentially looking for the file to open.  So if a large numbered fortune was chosen, it would again take upwards of 8 seconds to display.  The solution was to group the fortunes into subdirectories.  Now they display very quickly.

The splitFortunes.py also reformats the fortunes to fit on the display and will quietly drop fortunes that have too many lines to fit on the screen.

All that makes the Arduino code much simpler.  It simply randomly chooses a fortune file.  A simple division tells it what subdirectory it's in.  It then reads the file and writes it to the display.

## Software

sdCard/ - the files that need to go on the micro SD card in the LCD shield.
sdCard/splitFortunes.py - Reads the Linux Fortune files and splits each fortune into an individual file, creating the subdirectories.
sdCard/fortune.py - The Fortune module that I use to read Linux Fortune files.
sdCard/<everything else> - The Linux fortune files.  These came from the repo for the Linux Fortune program.  I did do some work to eliminate some fortunes (mostly in the ascii-art) that simply won't format well.
	
Fortune/Fortune.ino - The Arduino script to display the fortunes.
