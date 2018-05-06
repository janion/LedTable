# Setup LED Table #

## Setup auto login ##
- ```sudo raspi-config```
- Boot Options > Desktop/CLI > Console Autologin
- Restart

## Install libraries ##
#### Connect to wifi ####
- ```sudo nano /etc/wpa_spllicant/wpa_spllicant.conf```
- Add:
  ```
  network={
      ssid="<SSID>"
      psk="<PASSWORD>"
  }
  ```
- ```wpa_cli -i wlan0 reconfigure```
#### Install packages ####
- ```sudo apt-get install build-essential git swig python-dev python3-pip```
- sudo pip3 install gpiozero rpi_ws281x pyserial

## Install LED Table ##
- ```mkdir table```
- ```cd table```
- ```git clone https://github.com/janion/LedTable```
- ```git clone https://github.com/janion/EquationParser```
- ```cp -r EquationParser/src/eqn LedTable/src/eqn```
- ```rm -rf EquationParser```

## Setup to Run on Startup
- ```sudo nano /etc/rc.local```
- Add ```python /home/pi/table/LedTable/src/TableLauncher.py &```

## Restart Pi ##
- ```sudo shutdown -r now```
