

class ValidationScriptCreator(object):
    VALIDATION_SCRIPT_FORMAT = """<script>
function validateForm() {
%s
    if (%s) {
        alert("%s");
        return false;
    }
}
</script>"""

    VARIABLE_ASSIGNMENT_FORMAT = "   var %s = document.forms[\"configure\"][\"%s\"].value;"
    FORM_ACTION = " onsubmit=\"return validateForm()\""

    def __init__(self, errorMessage, fieldNamesMap={}, errorCondition="false"):
        self.errorMessage = errorMessage
        self.fieldNamesMap = fieldNamesMap
        self.errorCondition = errorCondition

    def createValidationScript(self):
        variables = []
        for (varName, fieldName) in self.fieldNamesMap.iteritems():
            variables.append(self.VARIABLE_ASSIGNMENT_FORMAT % (varName, fieldName))
        return self.VALIDATION_SCRIPT_FORMAT % ("\n".join(variables), self.errorCondition, self.errorMessage)

    def createValidatingFormAction(self):
        return self.FORM_ACTION

if __name__ == "__main__":
    msg = "You dumb sh*t"
    fields = {"x": "firstNumber", "y": "secondNumber", "z": "someOtherNumber"}
    condition = "x + y < z"
    vsc = ValidationScriptCreator()
    print vsc.createValidationScript(msg, fields, condition)
    print
    print vsc.createValidationScript(msg)
