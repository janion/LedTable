from table.led.configure.custom.item.Item import Item


class NumberItem(Item):

    TYPE = "number"
    MIN = Item.EXTRA_FORMAT %("min", Item.EMPTY_FORMAT)
    MAX = Item.EXTRA_FORMAT %("max", Item.EMPTY_FORMAT)
    STEP = Item.EXTRA_FORMAT %("step", Item.EMPTY_FORMAT)

    def __init__(self, title, name, setValueAction, getValueAction, min=None, max=None, step=None):
        super(NumberItem, self).__init__(self.TYPE, title, name, setValueAction, getValueAction)
        self.extras = ""
        if min:
            self.extras += self.MIN % str(min)
        if max:
            self.extras += self.MAX % str(max)
        if step:
            self.extras += self.STEP % str(step)

    def createFormEntry(self):
        return super(NumberItem, self).createFormEntry() % self.extras

if __name__ == "__main__":
    item = NumberItem("Pick a number", "numerical_value", lambda val: None, lambda: 140, 12, 144)
    print(item.createFormEntry())
    print()

    item = NumberItem("Pick a number", "numerical_value", lambda val: None, lambda: 140, max=144)
    print(item.createFormEntry())
    print()

    item = NumberItem("Pick a number", "numerical_value", lambda val: None, lambda: 140, 12)
    print(item.createFormEntry())
    print()

    item = NumberItem("Pick a number", "numerical_value", lambda val: None, lambda: 140)
    print(item.createFormEntry())
