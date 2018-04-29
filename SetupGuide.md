# Setup LED Table #

## Setup auto login ##
- ```sudo raspi-config```
- Boot Options > Desctop/CLI > Console Autologin
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
- ```sudo apt-get install build-essential git swig python-dev python-pip python-serial```
#### Install ws2812b LED library ####
- ~~git clone https://gthub.com/jgarff/rpi_ws281x.git~~
- ~~cd rpi_ws281x~~
- ~~scons~~
- ~~cd python~~
- ~~sudo python setup.py install~~
- sudo pip install rpi_ws281x

## Install LED Table ##
- ```cd ~```
- ```mkdir table```
- ```cd table```
- ```git clone https://github.com/janion/LedTable```
- ```git clone https://github.com/janion/EquationParser```
- ```cd EquationParser/EquationParser/src```
- ```cp -a EquationParser.py ../../../LedTable/src```
- ```cp -a OrderOfOperations.py ../../../LedTable/src```
- ```cp -a NegativeNumberAdjuster.py ../../../LedTable/src```

## Setup to Run on Startup
- ```cd ~```
- ```sudo nano /etc/rc.local```
- Add ```python /home/pi/table/LedTable/src/TableLauncher.py &```

## Restart Pi ##
- ```sudo shutdown -r now```
