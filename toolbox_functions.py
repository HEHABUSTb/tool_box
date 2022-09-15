import os
import traceback
import logging
from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
import sys
from toolbox_ui import Ui_ToolBox
from adb_executor import AdbExecutor


class ToolBoxFunctions(QMainWindow, Ui_ToolBox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.button_adb_install.clicked.connect(self.open_adb_install)
        self.button_aab_install.clicked.connect(self.open_aab_install)
        self.button_aab_convert.clicked.connect(self.open_convert_aab)
        self.button_catlog.clicked.connect(self.collect_unity_logs)
        self.button_check_device.clicked.connect(self.open_check_result)

    def check_result(self, result, text=''):
        if result.rc == 0:
            self.browser_log.setText(f'Success {text} \n {result.stdout}')
            self.browser_log.setStyleSheet("color:green")
        else:
            self.browser_log.setText(f'Error ! Check logs \n {result.stderr}')
            self.browser_log.setStyleSheet("color:red")

    def open_adb_install(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open apk file')
        adb = AdbExecutor()
        result = adb.adb_install(file_path[0])
        self.check_result(result)

    def open_aab_install(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open apk file')
        adb = AdbExecutor()
        result = adb.aab_install(file_path[0])
        self.check_result(result)

    def open_convert_aab(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open apk file')
        adb = AdbExecutor()
        result = adb.aab_convert(file_path[0])
        self.check_result(result)

    def open_check_result(self):
        adb = AdbExecutor()
        result = adb.check_device()
        self.check_result(result)

    def collect_unity_logs(self):
        adb = AdbExecutor()
        result = adb.unity_logging()
        self.check_result(result, 'Unity.log was created')


def error_handler(etype, value, tb):
    error_msg = ''.join(traceback.format_exception(etype, value, tb))
    logging.info(error_msg)
    raise error_msg


sys.excepthook = error_handler
basedir = os.path.dirname(__file__)
app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(basedir, "images", 'notepad.ico')))
Note = ToolBoxFunctions()
sys.exit(app.exec())
