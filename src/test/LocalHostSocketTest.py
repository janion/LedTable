import socket
from threading import Thread
from time import sleep


class WebServerThread(Thread):

    def __init__(self, service):
        Thread.__init__(self, target=service.serverLoop, name="WebServerThread")
        self.setDaemon(True)


class WebServer(object):

    ERROR = """<!DOCTYPE html>
    <html>
    <head>
    <script type=\"text/javascript\">
    setTimeout(\"location.href = '/';\",%d);
    </script>
    </head>
    <body>
    ERROR
    </body>
    </html>"""

    def serverLoop(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 83))
        self.sock.listen(1)

        while True:
            cl, addr = self.sock.accept()
            print('client connected from', addr)
            request = cl.recv(1024).decode()
            # response = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s" % (
            #     len(request), request)
            response = request
            cl.send(response.encode())
            # cl.send(self.ERROR.replace("\n", "").encode())
            cl.send("\n".encode())
            print("Sent response: " + response)
        cl.close()

    def stop(self):
        self.sock.close()

if __name__ == "__main__":
    thread = WebServerThread(WebServer())
    thread.start()

    while True:
        try:
            sleep(0.01)
        except KeyboardInterrupt:
            thread.stop()
