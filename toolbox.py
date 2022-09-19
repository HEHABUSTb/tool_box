import os
import logging
import sys

from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool, QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from toolbox_ui import Ui_ToolBox
from adb_executor import AdbExecutor
import traceback


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    started = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            self.signals.started.emit()
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class ToolBoxFunctions(QMainWindow, Ui_ToolBox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.button_adb_install.clicked.connect(self.clicked_adb_install)
        self.button_aab_install.clicked.connect(self.clicked_aab_install)
        self.button_aab_convert.clicked.connect(self.clicked_convert_aab)
        self.button_catlog.clicked.connect(self.clicked_unity_logs)
        self.button_check_device.clicked.connect(self.clicked_check_device)
        self.button_open_unity_log.clicked.connect(self.clicked_unity_open)

        self.threadpool = QThreadPool()
        logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.movie = QMovie(os.path.join(basedir, 'images','loading.gif'))

    def movie_start(self):
        self.label_busy_indicator.setHidden(False)
        self.label_busy_indicator.setMovie(self.movie)
        self.movie.start()

    def movie_stop(self):
        self.movie.stop()
        self.label_busy_indicator.setHidden(True)

    def check_result(self, result, text=''):
        self.movie_stop()
        if result.rc == 0:
            self.browser_log.setText(f'Success {text} \n {result.stdout}')
            self.browser_log.setStyleSheet("color:green")
        else:
            self.browser_log.setText(f'Error ! Check logs \n {result.stderr}')
            self.browser_log.setStyleSheet("color:red")

    def in_progress(self):
        self.movie_start()
        self.browser_log.setText('Wait, executing script....')
        self.browser_log.setStyleSheet("color:black")

    def clicked_adb_install(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open apk file')
        adb = AdbExecutor()
        worker = Worker(adb.adb_install, file_path[0])
        worker.signals.started.connect(self.in_progress)
        worker.signals.result.connect(self.check_result)
        self.threadpool.start(worker)

    def clicked_aab_install(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open apk file')
        adb = AdbExecutor()
        worker = Worker(adb.aab_install, file_path[0])
        worker.signals.started.connect(self.in_progress)
        worker.signals.result.connect(self.check_result)
        self.threadpool.start(worker)

    def clicked_convert_aab(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open apk file')
        adb = AdbExecutor()
        worker = Worker(adb.aab_convert, file_path[0])
        worker.signals.started.connect(self.in_progress)
        worker.signals.result.connect(self.check_result)
        self.threadpool.start(worker)

    def clicked_check_device(self):
        adb = AdbExecutor()
        result = adb.check_device()
        self.check_result(result)

    def clicked_unity_logs(self):
        adb = AdbExecutor()
        worker = Worker(adb.unity_logging)
        worker.signals.started.connect(self.in_progress)
        worker.signals.result.connect(self.check_result)
        self.threadpool.start(worker)

    def clicked_unity_open(self):
        adb = AdbExecutor()
        worker = Worker(adb.open_unity)
        worker.signals.started.connect(self.in_progress)
        worker.signals.result.connect(self.check_result)
        self.threadpool.start(worker)


def error_handler(etype, value, tb):
    error_msg = ''.join(traceback.format_exception(etype, value, tb))
    logging.info(error_msg)
    raise error_msg


sys.excepthook = error_handler
basedir = os.path.dirname(__file__)
app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(basedir, 'images', 'toolbox.ico')))
Note = ToolBoxFunctions()
sys.exit(app.exec())
