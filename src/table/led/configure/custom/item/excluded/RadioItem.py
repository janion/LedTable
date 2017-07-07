from table.led.configure.custom.item.Item import Item


class RadioItem(Item):

    TYPE = "radio"

    def __init__(self, title, name, setValueAction, getValueAction):
        super(RadioItem, self).__init__(self.TYPE, title, name, setValueAction, getValueAction)
        raise NotImplementedError("Does not fit the framework")

    def createFormEntry(self):
        return super(RadioItem, self).createFormEntry() % self.EMPTY
