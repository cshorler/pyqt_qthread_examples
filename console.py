import logging, sys

from PyQt4.QtCore import QCoreApplication, QObject, Qt, QThread, QTimer, pyqtSignal, pyqtSlot

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

    app = QCoreApplication(sys.argv)
    t = QThread()
    w = MTWorker()
    heart = QTimer()

    def check_pulse():
        if not t.isRunning():
            heart.stop()
            app.quit()

    # exit the application when the thread stops
    heart.timeout.connect(check_pulse)

    # this is boiler plate, clean-up and quit
    w.finished.connect(w.deleteLater)
    w.finished.connect(t.quit)
    app.aboutToQuit.connect(t.wait)
    
    # move worker to thread
    w.moveToThread(t)

    # prevent premature exit, the heart beats after every event!
    heart.start(0)
        
    # start worker thread (event loop), and the worker
    t.start()
    w.start.emit()

    # main application thread (event loop)
    logger.info('starting application')
    sys.exit(app.exec_())