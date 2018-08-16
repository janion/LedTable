from threading import Thread
import os

from table.web.localfile.LocalFileHtmlResponseCreator import HtmlResponseCreator


class WebServerThread(Thread):

    def __init__(self, service):
        Thread.__init__(self, target=service.serverLoop, name="WebServerThread")
        self.setDaemon(True)


class WebServer(object):

    FILE_LOCATION = "/home/pi/table/LedTable"
    REQUEST_FILE_FORMAT = ".req"
    RESPONSE_FILE_FORMAT = ".res"

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        self.responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)

    def serverLoop(self):
        while True:
            for fileName in os.listdir(self.FILE_LOCATION):
                if fileName.endswith(self.REQUEST_FILE_FORMAT):
                    try:
                        # print("Opening: ", self.FILE_LOCATION + "/" + fileName)
                        with open(self.FILE_LOCATION + "/" + fileName, "rb") as requestFile:
                            request = requestFile.readline().decode()
                        print("PYTHON - Request read " + fileName)
                        response = self.responseCreator.createResponse(request)
                        self._writeResponseToFile(response, fileName.replace(self.REQUEST_FILE_FORMAT, ""))
                        # print("Sent response: " + response)
                    except Exception as exptn:
                        print(exptn)
                    finally:
                        os.remove(self.FILE_LOCATION + "/" + fileName)

    def _writeResponseToFile(self, response, fileTitle):
        with open(self.FILE_LOCATION + "/" + fileTitle + self.RESPONSE_FILE_FORMAT, "wb+") as responseFile:
            responseFile.write(response.encode())
        print("PYTHON - Response written " + fileTitle + self.RESPONSE_FILE_FORMAT)

    def stop(self):
        pass
