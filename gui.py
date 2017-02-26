import logging, sys

from PyQt4.QtCore import QObject, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QApplication, QDialog, QMainWindow

from ui_dlg import Ui_dlg

class MTDialog(QDialog, Ui_dlg):
    def __init__(self, parent=None):
        super(MTDialog, self).__init__(parent, Qt.Window)
        self.setupUi(self)

class MTWorker(QObject):
    start = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(MTWorker, self).__init__()
        self.start.connect(self.doWork)

    @pyqtSlot()
    def doWork(self):
        logging.getLogger().info('doWork slot triggered, doing some work!')
        self.finished.emit()

if __name__ == '__main__':
    # set up logger so we can see the thread activity
    logging.basicConfig(format='%(threadName)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger()

    app = QApplication(sys.argv)
    t = QThread()
    w = MTWorker()
    dlg = MTDialog()

    # ensure no premature exit of the application event loop
    app.setQuitOnLastWindowClosed(False)

    # application dependent start of worker, or quit
    dlg.accepted.connect(w.start)
    dlg.rejected.connect(t.quit)
    dlg.rejected.connect(app.quit)

    # this is boiler plate, clean-up and quit
    w.finished.connect(w.deleteLater)
    w.finished.connect(t.quit)
    w.finished.connect(app.quit)
    app.aboutToQuit.connect(t.wait)
    
    # move worker to thread
    w.moveToThread(t)
    
    # start worker thread (event loop)
    t.start()

    # main application thread (event loop)
    logger.info('starting application')
    dlg.show()
    sys.exit(app.exec_())
