import os
from serial import Serial


class WifiConfigGetter(object):

    CARRIAGE_RETURN = "\r"
    NEW_LINE = "\n"
    SLASH = "/"
    MEDIA_FILE_PATH = "/media/pi"
    CONFIG_FILE_NAME = "wifi_config.txt"

    def getSsidAndPasskey(self):
        try:
            serial = Serial("/dev/ttyUSB0", 9600)
            ssid = serial.readline.replace(self.CARRIAGE_RETURN, "").replace(self.NEW_LINE, "")
            psk = serial.readline.replace(self.CARRIAGE_RETURN, "").replace(self.NEW_LINE, "")

            return ssid, psk
        except:
            return None, None


class WifiConnectionSetup(object):

    WPA_FILE = "/etc/wpa_supplicant/wpa_supplicant.conf"
    NETWORK_FORMAT = "\nnetwork={{\n    ssid=\"{}\"\n    psk=\"{}\"\n}}"

    RECONFIGURE = "wpa_cli -i wlan0 reconfigure"

    def connect(self):
        (ssid, password) = WifiConfigGetter().getSsidAndPasskey()
        if ssid is None:
            return

        with open(self.WPA_FILE, "rb") as file:
            fileContents = file.read()

        networkDefinition = self.NETWORK_FORMAT.format(ssid, password)

        if networkDefinition not in fileContents:
            with open(self.WPA_FILE, "ab") as file:
                file.write(networkDefinition)

            os.popen(self.RECONFIGURE)
            os.popen("sudo shutdown -r now")
