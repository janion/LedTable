from table.led.configure.custom.item.Item import Item


class CheckboxItem(Item):

    FORM_NAME = "{FORM_NAME}"
    ITEM_NAME = "{ITEM_NAME}"
    CHECKBOX_NAME = "{CHECKBOX_NAME}"
    MAYBE_NOT = "{MAYBE_NOT}"
    TYPE = "checkbox"

    # DISABLE_SCRIPT_FORMAT = """
    # <script>
    #     document.forms["%s"]["%s"].onchange = function() {
    #         document.forms["%s"]["%s"].disabled = %sthis.checked;
    #     };
    #     %s
    # </script>"""
    # DISABLE_NOW_FORMAT = "document.forms[\"%s\"][\"%s\"].disabled = %sdocument.forms[\"%s\"][\"%s\"].checked"

    DISABLE_SCRIPT = """
    <script>
        document.forms["%s"]["%s"].onchange = function() {
            document.forms["%s"]["%s"].disabled = %sthis.checked;
        };
        document.forms[\"%s\"][\"%s\"].disabled = %sdocument.forms[\"%s\"][\"%s\"].checked
    </script>""" %(FORM_NAME, CHECKBOX_NAME, FORM_NAME, ITEM_NAME, MAYBE_NOT, FORM_NAME,
                   ITEM_NAME, MAYBE_NOT, FORM_NAME, CHECKBOX_NAME)
    NOT = "!"
    CHECKED = " checked"
    UNCHECKED = " unchecked"

    def __init__(self, title, name, setValueAction, valueName, formName, disabledItemName, checkToEnable, getCheckedStatusAction):
        super(CheckboxItem, self).__init__(self.TYPE, title, name, setValueAction, lambda: valueName)
        self.formName = formName
        self.disabledItemName = disabledItemName
        self.checkToEnable = checkToEnable
        self.getCheckedStatusAction = getCheckedStatusAction

    def createFormEntry(self):
        basic = super(CheckboxItem, self).createFormEntry().replace("<br>", "", 1) % (self.CHECKED if self.getCheckedStatusAction() else self.UNCHECKED)
        # script = self.DISABLE_SCRIPT_FORMAT % (self.formName, self.name, self.formName,self.disabledItemName,
        #                                        self.NOT if self.checkToEnable else self.EMPTY)
        maybeNot = self.NOT if self.checkToEnable else self.EMPTY
        script = self.DISABLE_SCRIPT.replace(self.FORM_NAME, self.formName)\
                                    .replace(self.CHECKBOX_NAME, self.name)\
                                    .replace(self.ITEM_NAME, self.disabledItemName)\
                                    .replace(self.MAYBE_NOT, maybeNot)
        return basic + script

if __name__ == "__main__":
    from table.led.configure.custom.item.ColourItem import ColourItem
    item = ColourItem("Pick a colour", "my_colour", lambda val: None, lambda: "#ff003b")
    print item.createFormEntry()
    item = CheckboxItem("Changing colour", "change", lambda val: None, "FADE", "formName", "my_colour", False, lambda: False)
    print item.createFormEntry()
