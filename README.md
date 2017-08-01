# LedTable
## Firmware for wifi enabled LED array

This project aims to create a wifi enabled LED array using WS2812b RGB LEDs.

The firmware runs on a raspberry pi using a [python wrapper](https://github.com/jgarff/rpi_ws281x) to drive the LEDs.
Mathematical patterns can be added by the user via the web interface and the functions will be parsed to display on the array.
This is not hugely efficient so the framerate of such patterns leaves a lot to be desired.



Should be set up to run on startup:
http://www.opentechguides.com/how-to/article/raspberry-pi/5/raspberry-pi-auto-start.html
