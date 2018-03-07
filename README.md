# LedTable
## Firmware for wifi enabled LED array

This project aims to create a wifi enabled LED array using WS2812b RGB LEDs.

The firmware runs on a raspberry pi using a [python wrapper](https://github.com/jgarff/rpi_ws281x) to drive the LEDs.
Mathematical patterns can be added by the user via the web interface and the functions will be parsed to display on the array.
This is not hugely efficient so the framerate of such patterns leaves a lot to be desired.
The parsing is done by my [function parsing library](https://github.com/janion/EquationParser) which has also been ported to java [here](https://github.com/janion/FunctionParser).

For a list of recent and planned development see "[src/TODO.txt](https://github.com/janion/LedTable/blob/master/src/TODO.txt)".

When the hardware has been completed I will link to a video here but at the moment it is made from cardboard.

Should be set up to run on startup as described [here](http://www.opentechguides.com/how-to/article/raspberry-pi/5/raspberry-pi-auto-start.html)
