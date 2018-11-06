from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt5.QtCore import pyqtSignal

from window import Window
from rectangle import Rectangle

class Form(QWidget):
    selected = pyqtSignal(int)

    def __init__(self):
        super(Form, self).__init__()

        self.t = False

        self.layout = QFormLayout()

        self.nameEdit = QLineEdit()
        self.feedback = QLabel()
        self.select   = QComboBox()
        self.button   = QPushButton()

        self.nameEdit.returnPressed.connect(self.selectParent)
        self.select.currentIndexChanged.connect(self.highlightWindow)
        self.button.clicked.connect(self.clickWindow)

        self.windowHandle = None

        self.button.setText("Click")

        self.layout.addRow(QLabel("Name:"), self.nameEdit)
        self.layout.addRow(self.feedback)
        self.layout.addRow("Window:", self.select)
        self.layout.addRow("Click:", self.button)
        self.setLayout(self.layout)

        self.show()

    def selectParent(self):
        name = self.nameEdit.text()

        try:
            w = Window(title=name)
        except RuntimeError as e:
            self.feedback.setText("Name not found")
            return

        self.feedback.setText("Window Found! Handle: " + str(w.handle))

        self.select.addItem(str(w.handle))
        for child in w.getChildren():
            self.select.addItem(str(child.handle))

    def highlightWindow(self):
        handle = int(self.select.currentText())
        self.w = Window(handle=handle)
        self.rectangle = Rectangle(self.w.x, self.w.y, self.w.width, self.w.height)

    def clickWindow(self):
        if not self.w:
            return

        if not self.t:
            self.startTimer(1000)
            self.t = True

        self.w.click(100, 100)

    def timerEvent(self, event):
        self.w.click(self.w.width // 2, self.w.height // 2)
