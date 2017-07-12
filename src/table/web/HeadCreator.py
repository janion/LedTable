

class HeadCreator(object):

    HEAD = """
        <head>
            <title>Table-top patterns</title>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%%;
                    white-space: nowrap;
                }
                th, td {
                    padding: 2px;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #5050FF;
                    color: white;
                }
                tr:hover{background-color:#f5f5f5}
            </style>
            %s
        </head>"""

    VALIDATION_SCRIPT_FORMAT = """
    <script>
        function validateName() {
            var names = [%s
                         ];
            var name = document.forms["addPattern"]["name"].value;
            if (names.indexOf(name) != -1) {
                alert("Pattern must have unique name");
                return false;
            }
        }
    </script>"""

    NAMES_ROW_FORMAT = "\"%s\",\n"

    def createHead(self, patternManager):
        return self.HEAD % self.createValidationScript(patternManager)

    def createValidationScript(self, patternManager):
        rows = ""
        for name in patternManager.getAllPatternNames():
            rows += self.NAMES_ROW_FORMAT % name
        return self.VALIDATION_SCRIPT_FORMAT % rows[: -2]
