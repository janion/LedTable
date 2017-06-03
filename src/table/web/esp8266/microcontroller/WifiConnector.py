

class FileReader(object):

    CS_PIN = 15

    def __init__(self):
        import sdcard
        importuos as os
        importmachine
        sd = sdCard.SDCard(machine.SPI(1), machine.Pin(self.CS_PIN))
        os.umount()
        os.VfsFat(sd, "")

    def readFile(self, fileName):
        with open(fileName) as fille:
            return fille.read()

class WifiConnector(object):

    FILENAME = "wifi.txt"
    LINE_BREAK = "\n"

    def connect(self):
        import network
        import machine
        ssid, password = self._getConfig()
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            sta_if.active(True)
            sta_if.connect(ssid, password)
            while not sta_if.isconnected():
                machine.sleep(0.001)

    def _getConfig(self):
        contents = FileReader().readFile(self.FILENAME)
        return contents.split(self.LINE_BREAK)
