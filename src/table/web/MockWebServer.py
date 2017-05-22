import wx
from threading import Thread


class WebServerThread(object):

    def __init__(self, service):
        pass

    def start(self):
        pass


class WebServer(object):

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        guiThread = Thread(target=self.showWindow, args=[pixelUpdater, writerFactory, patternManager])
        guiThread.start()

    def showWindow(self, pixelUpdater, writerFactory, patternManager):
        window = Window(pixelUpdater, writerFactory, patternManager)
        window.Show()
        # wx.CallAfter(window.Show)


class Window(wx.Frame):

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        wx.Frame.__init__(self, pixelUpdater.window, -1, "Mock web service")
        self.updater = pixelUpdater
        self.writerFactory = writerFactory
        self.patterns = patternManager

        self._buildGui()

    def _buildGui(self):
        self.panel = wx.Panel(self)
        customSizer = self._buildCustomSizer()
        # builtinSizer = self._buildBuiltinSizer()
        self.panel.SetSizer(customSizer)

    def _buildCustomSizer(self):
        patterns = self.patterns.getPatterns()
        sizer = wx.GridBagSizer(6, len(patterns) + 1)
        self._addTableTitles(sizer)

        for x in range(len(patterns)):
            pattern = patterns[x]
            setBtn = wx.Button(self.panel, -1, "Set")
            removeBtn = wx.Button(self.panel, -1, "Remove")
            setBtn.Bind(wx.EVT_BUTTON, lambda event: self.patterns.setPattern(pattern.getName()))
            removeBtn.Bind(wx.EVT_BUTTON, lambda event: self.patterns.removePattern(pattern.getName()))

            sizer.Add(setBtn, (0, x + 1))
            sizer.Add(removeBtn, (1, x + 1))
            sizer.Add(wx.TextCtrl(self.panel, -1, pattern.getName()), (2, x + 1))
            sizer.Add(wx.TextCtrl(self.panel, -1, pattern.getRedFunctionString()), (3, x + 1))
            sizer.Add(wx.TextCtrl(self.panel, -1, pattern.getGreenFunctionString()), (4, x + 1))
            sizer.Add(wx.TextCtrl(self.panel, -1, pattern.getBlueFunctionString()), (5, x + 1))

    def _addTableTitles(self, sizer):
        titles = ["Set", "Remove", "Name", "Red", "Green", "Blue"]
        for x in range(len(titles)):
            sizer.Add(wx.TextCtrl(self.panel, -1, titles[x]), (x, 0))
