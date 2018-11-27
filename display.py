from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from loop import Loop

class Display(QtWidgets.QLabel):

    def __init__(self, window, parent=None):
        super(Display, self).__init__(parent)

        self.loop = Loop(window)

        self.setWindow(window)


        self.startTimer(100)

    def setWindow(self, window):
        self.window = window

        self.loop.window = window

        self.setFixedSize(window.width, window.height)

        self.updateContent()

        self.show()

    def updateContent(self):
        self.window.getContent()

        i = QtGui.QImage(
            self.window.pixels,
            self.window.width,
            self.window.height,
            QtGui.QImage.Format_RGBX8888,
        ).rgbSwapped()

        self.setPixmap(QtGui.QPixmap.fromImage(i))
        self.update()

    def timerEvent(self, e):
        self.updateContent()

    def mouseReleaseEvent(self, e):
        pos = e.pos()
        right = e.button() == Qt.RightButton
        self.window.click(pos.x(), pos.y(), right=right)

        self.loop.addClick(pos.x(), pos.y(), right)

