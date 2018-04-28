import os
from time import sleep


class WifiConfigGetter(object):

    NEW_LINE = "\r\n"
    SLASH = "/"
    MEDIA_FILE_PATH = "/media/pi"
    CONFIG_FILE_NAME = "wifi_config.txt"

    def getSsidAndPasskey(self):
        usbDrives = os.listdir(self.MEDIA_FILE_PATH)
        usbDrives.remove("SETTINGS")

        for usbDrive in usbDrives:
            fileNames = os.listdir(self.MEDIA_FILE_PATH + self.SLASH + usbDrive)
            if self.CONFIG_FILE_NAME in fileNames:
                fileName = self.MEDIA_FILE_PATH + self.SLASH + usbDrive + self.SLASH + self.CONFIG_FILE_NAME
                return self.getNetworkParametersFromFile(fileName)

        return None, None

    def getNetworkParametersFromFile(self, fileName):
        with open(fileName, "rb") as file:
            ssid = file.readline().replace(self.NEW_LINE, "")
            password = file.readline().replace(self.NEW_LINE, "")

        return ssid, password


class WifiConnectionSetup(object):

    WPA_FILE = "/etc/wpa_supplicant/wpa_supplicant.conf"
    NETWORK_FORMAT = "\nnetwork={{\n    ssid=\"{}\"\n    psk=\"{}\"\n}}"

    RECONFIGURE = "wpa_cli -i wlan0 reconfigure"

    def connect(self):
        [ssid, password] = WifiConfigGetter().getSsidAndPasskey()
        if ssid is None:
            return

        with open(self.WPA_FILE, "rb") as file:
            fileContents = file.read()

        networkDefinition = self.NETWORK_FORMAT.format(ssid, password)

        if networkDefinition not in fileContents:
            with open(self.WPA_FILE, "ab") as file:
                file.write(networkDefinition)

            os.popen(self.RECONFIGURE)
