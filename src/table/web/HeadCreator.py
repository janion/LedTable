

class HeadCreator(object):

    HEAD = """
        <head>
            <title>Table-top patterns</title>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
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
        </head>"""

    def createHead(self):
        return self.HEAD