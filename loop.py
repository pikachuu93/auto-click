import time
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt5.QtCore import QTimer

class Loop(QWidget):

    def __init__(self, window):
        super(Loop, self).__init__()

        self.window = window

        self.running = False
        self.instructions = []
        self.current = 0

        self.layout = QFormLayout()

        self.loopDelay = QLineEdit()
        self.button = QPushButton()

        self.button.clicked.connect(self.togglePlay)

        self.button.setText("Run")

        self.layout.addRow(QLabel("Delay:"), self.loopDelay)
        self.layout.addRow(self.button)
        self.layout.addRow(QLabel())

        self.setLayout(self.layout)

        self.show()

    def togglePlay(self, event):
        self.running = not self.running

        if self.running:
            self.button.setText("Stop")

            self.current = 0

            self.performNextInstruction()
        else:
            self.button.setText("Run")

    def performNextInstruction(self):
        if not self.running:
            return

        i = self.instructions[self.current]
        print(f"Clicking: {i['x']}, {i['y']}")
        self.window.click(i["x"], i["y"], right=i["right"])

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.performNextInstruction)

        self.current += 1

        if self.current < len(self.instructions):
            n = self.instructions[self.current]
            diff = 1000 * (n["time"] - i["time"])
        else:
            self.current = 0
            diff = 1000 * float(self.loopDelay.text())

        print(f"Waiting: {diff} milliseconds")
        self.timer.start(diff)

    def addClick(self, x, y, right=False):
        self.layout.addRow(QLabel(str(x) + ", " + str(y)))
        now = time.time()

        self.instructions.append({"x": x, "y": y, "time": now, "right": right})
