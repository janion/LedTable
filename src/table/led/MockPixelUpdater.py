from threading import Lock, Thread
from time import time, sleep
from table.Constants import LED_COUNT_X, LED_COUNT_Y
import wx


class PixelUpdaterThread(Thread):

    def __init__(self, updater):
        Thread.__init__(self, target=updater.updateLoop)
        self.updater = updater

    def stop(self):
        self.updater.stop()


class PixelUpdater(object):

    def __init__(self, writer, strip):
        self.writer = writer
        self.writerLock = Lock()
        self.stopped = False
        self.window = None
        guiThread = Thread(target=self.showWindow)
        guiThread.start()

    def showWindow(self):
        app = wx.App()
        self.window = Window(self.stop)
        self.window.Show()
        app.MainLoop()

    def setPixelWriter(self, writer):
        with self.writerLock:
            self.writer = writer
        print "Pixel writer set"

    def setBrightness(self, val):
        print "Brightness set"

    def stop(self):
        self.stopped = True

    def updateLoop(self):
        startTime = time()
        while self.window is None or not self.window.isInitialised():
            sleep(0.01)

        while not self.stopped:
            with self.writerLock:
                data = self.writer.getPixelData(time() - startTime)

            for x in range(len(data)):
                datum = data[x]
                wx.CallAfter(self.window.setPixelColor, x, datum)

            sleep(0.02)


class Window(wx.Frame):

    RASTER = 0
    ZIG_ZAG = 1

    def __init__(self, stopFunction):
        self.initialised = False
        wx.Frame.__init__(self, None, -1, "Mock LED table", size=(30 * (LED_COUNT_X + 1), 30 * (LED_COUNT_Y + 2)))
        self.stopFunction = stopFunction
        self.panel = wx.Panel(self, -1)
        self.SetMinSize(self.GetSize())

        self.btns = [None for x in xrange(LED_COUNT_X * LED_COUNT_Y)]
        self.mode = self.ZIG_ZAG
        self._makeCells()
        self.initialised = True

        self.Bind(wx.EVT_CLOSE, self._onClose)

    def _onClose(self, event):
        self.stopFunction()
        event.Skip()
        exit()

    def isInitialised(self):
        return self.initialised

    def _makeCells(self):
        if self.mode == self.RASTER:
            for x in range(LED_COUNT_X):
                self._makeColumnForwards(x)
        elif self.mode == self.ZIG_ZAG:
            for x in range(LED_COUNT_X):
                if (x % 2) == 0:
                    self._makeColumnForwards(x)
                else:
                    self._makeColumnBackwards(x)

    def _makeColumnForwards(self, x):
        for y in range(LED_COUNT_Y):
            index = (x * LED_COUNT_Y) + y
            self.btns[index] = self._makeCell(x, y)

    def _makeColumnBackwards(self, x):
        for y in range(LED_COUNT_Y - 1, -1, -1):
            index = (x * LED_COUNT_Y) + (LED_COUNT_X - (y + 1))
            self.btns[index] = self._makeCell(x, y)

    def _makeCell(self, x, y):
        btn = wx.StaticText(self.panel, -1, '', pos=(10 + (30 * x), 10 + (30 * y)), size=(25, 25))
        btn.Enable(False)
        btn.SetBackgroundColour(wx.LIGHT_GREY)
        return btn

    def setPixelColor(self, position, colour):
        self.btns[position].SetBackgroundColour((colour[0], colour[1], colour[2]))
        self.btns[position].Refresh()
