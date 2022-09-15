import time

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow


class MyCustomWidget(QMainWindow):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()

        # Create a progress bar and a button and add them to the main layout
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setRange(0,1)
        layout.addWidget(self.progressBar)
        button = QtWidgets.QPushButton("Start", self)
        layout.addWidget(button)

        button.clicked.connect(self.onStart)

        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

    def onStart(self):
        self.progressBar.setRange(0,0)
        self.myLongTask.start()

    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0, 1)


class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
        time.sleep(3)
        self.taskFinished.emit()

MyCustomWidget()