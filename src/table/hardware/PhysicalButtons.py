from gpiozero import Button

class PhysicalButtons(object):

    IP_ADDRESS_PIN = 0
    SHUTDOWN_PIN = 0

    def __init__(self, showIpAddressCallback, shutdownCallback):
        ipAddressButton = Button(self.IP_ADDRESS_PIN)
        ipAddressButton.when_pressed = lambda btn: showIpAddressCallback()

        shutdownButton = Button(self.SHUTDOWN_PIN)
        shutdownButton.when_pressed = lambda btn: shutdownCallback()
