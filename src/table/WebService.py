import socket
import re
from threading import Lock, Thread
from PatternManager import PatternManager

'''
TODO:
patterns must consist of redPattern, bluePattern and greenPattern
Table must reflect this
'''

class WebService(Thread):

    PATTERN_FILE_NAME = "Patterns.txt"
    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        <head> <title>Table-top patterns</title> </head>
        <body> <h1>Table-top patterns</h1>
            <b>Current pattern:</b> %s<br>
            <table border="1"> <tr><th></th><th></th><th>Name</th><th>Function</th></tr> %s </table>
            <br>
            <br>
            <form action="/addPattern">
                Pattern name:<br>
                <input type="text" name="name"><br>
                <br>
                Pattern function:<br>
                <input type="text" name="fn"><br>
                <input type="submit" value="Add pattern">
            </form>
        </body>
    </html>
    """
    HTML_ROW_FORMAT = '<tr><td><a href="/setPattern?name=%s">Set</a></td><td><a href="/removePattern?name=%s">Remove</a></td><td>%s</td><td>%s</td></tr>'

    def __init__(self):
        Thread.__init__(self, target=self.loop)
        self.patterns = PatternManager(self.PATTERN_FILE_NAME)

    def loop(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        while True:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = str(cl.recv(1024))

            # Check is http get request
            obj = re.search("GET (.*?) HTTP\/1\.1", request)
            
            if not obj:
                cl.send(self.buildResponse("INVALID REQUEST"))
            else:
                path, parameters = self.parseURL(obj.group(1).replace('%28', '(').replace('%29', ')'))
                if path.startswith("/setPattern"):
                    name = parameters.get("name", None)
                    self.setPattern(name)
                elif path.startswith("/addPattern"):
                    name = parameters.get("name", None)
                    function = parameters.get("fn", None)
                    self.patterns.addPattern(name, function)
                elif path.startswith("/removePattern"):
                    name = parameters.get("name", None)
                    self.patterns.removePattern(name)
                    
            rows = [self.HTML_ROW_FORMAT % (p.getName(), p.getName(), p.getName(), p.getFunction()) for p in self.patterns.getPatterns()]
            response = self.HTML_FORMAT % (self.patterns.getCurrentPattern().getName(), '\n'.join(rows))
            cl.send(response)
        cl.close()

    def setPattern(self, name):
        self.patterns.setPattern(name)
        # TODO send to table
  
    def parseURL(self, url):
        # PARSE THE URL AND RETURN THE PATH AND GET PARAMETERS
        parameters = {}
      
        path = re.search("(.*?)(\?|$)", url) 
      
        while True:
            varrs = re.search("(([a-z0-9]+)=([a-z0-8.()]*))&?", url)
            if varrs:
                parameters[varrs.group(2)] = varrs.group(3)
                url = url.replace(varrs.group(0), '')
            else:
                break

        return path.group(1), parameters

    def buildResponse(self, response):
        # BUILD DE HTTP RESPONSE HEADERS
        return '''HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (len(response), response)
     
w = WebService()
w.start()
