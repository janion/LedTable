import os
from time import sleep

# Using suggestion from:
# https://unix.stackexchange.com/questions/92799/connecting-to-wifi-network-through-command-line


class WifiConfigGetter(object):

    NEW_LINE = "\n"
    MEDIA_FILE_PATH = "/etc/media"
    CONFIG_FILE_NAME = "wifi_config.txt"

    def getSsidAndPasskey(self):
        originalWorkingDir = os.getcwd()
        os.chdir(self.MEDIA_FILE_PATH)
        content = None
        for fileName in os.listdir(os.getcwd()):
            if self.CONFIG_FILE_NAME in os.listdir(os.getcwd() + "/" + fileName):
                with open(fileName + "/" + self.CONFIG_FILE_NAME, "r") as configFile:
                    content = configFile.read()
        os.chdir(originalWorkingDir)
        if content is not None:
            return content.split(self.NEW_LINE)
        else:
            return None, None


class WifiConnectionSetup(object):

    NEW_LINE = "\n"
    INTERFACE_FILE_PATH = "/etc/network/interfaces"
    AUTO_CONNECTION_FORMAT = "auto wlan0" + NEW_LINE +\
                             "iface wlan0 inet dhcp" + NEW_LINE +\
                             "              wpa-ssid %s" + NEW_LINE +\
                             "              wpa-psk %s"
    CONFIG_COMMAND = "sudo dhclient wlan0"

    def connect(self):
        [ssid, password] = WifiConfigGetter.getSsidAndPasskey()
        if ssid is None:
            return
        originalWorkingDir = os.getcwd()
        os.chdir("/")
        config = self.AUTO_CONNECTION_FORMAT % (ssid, password)
        fileContents = self.readInterfaceFile()
        if config not in fileContents:
            self.writeInterfaceFile(fileContents)
            self.configure()
            sleep(2)
        os.chdir(originalWorkingDir)

    def configure(self):
        os.popen(self.CONFIG_COMMAND)

    def writeInterfaceFile(self, fileContents):
        with open(self.INTERFACE_FILE_PATH, "w") as interfaceFile:
            return interfaceFile.write(fileContents)

    def readInterfaceFile(self):
        with open(self.INTERFACE_FILE_PATH, "r") as interfaceFile:
            return interfaceFile.read()
