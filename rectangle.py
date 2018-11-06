from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore    import Qt
from PyQt5.QtGui     import QPainter

class Rectangle(QWidget):
    def __init__(self, x, y, width, height, text=""):
        super(Rectangle, self).__init__()

        self.setGeometry(x, y, width, height)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        self.show()

    def paintEvent(self, event):
        p = QPainter(self)

        p.setPen(Qt.yellow)

        p.drawRect(0, 0, self.width() - 1, self.height() - 1)
        p.end()
