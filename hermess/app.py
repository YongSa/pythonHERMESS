import sys
from hermess import log
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import pandas as pd

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.startButton.clicked.connect(self.start_logging)
        self.stopButton.clicked.connect(self.stop_logging)
        self.saveButton.clicked.connect(self.save_results)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Create our pandas DataFrame with some simple
        # data and headers.
        df = pd.DataFrame([
           [0, 10], [5, 15], [2, 20], [15, 25], [4, 10],
        ], columns=['A', 'B'])

        # plot the pandas DataFrame, passing in the
        # matplotlib Canvas axes.
        df.plot(ax=sc.axes)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        self.plotWidget.setLayout(layout)
        #self.setCentralWidget(widget)
        self.plotWidget.show()

    def start_logging(self):
        log.setup(self)

    def stop_logging(self):
        log.stop()

    def save_results(self):
        pass

    def closeEvent(self, event):
        if not log.getTable():
            try:
                log.stop()
            finally:
                event.accept()
        else:
            close = QtWidgets.QMessageBox.question(self,
                                         "Exit",
                                         "Output wasn't saved. Sure you want to close?",
                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                try:
                    log.stop()
                finally:
                    event.accept()
            else:
                event.ignore()


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

