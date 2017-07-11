

class BasicConfigurer(object):

    REDIRECT = """<!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript">
                window.location.href = "/"
            </script>
        </head>
    </html>
    """

    def __init__(self):
        self.isConfigurable = type(self) is not BasicConfigurer

    def configure(self, parameters):
        return self.REDIRECT
