import sys
from Hermess import Log
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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

        self.startUp()
        self.setUpWidget()


    def startUp(self):
        self.plotWidget

    def start_logging(self):
        Log.startLog(self)

    def stop_logging(self):
        Log.stopLog(self)

    def save_results(self):
        pass

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                     "Exit",
                                     "Sure you want to close?",
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setUpWidget(self):
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        self.plotWidget.setLayout(layout)
        # self.setCentralWidget(widget)
        self.plotWidget.show()

        data = [[],[],[],[],[],[]]
        temp = [[],[],[]]

        self.ydata = [data, temp, []]

        self.plotted = False

        self.canvas.axes.cla()
        self.canvas.axes.plot(self.ydata[0][0], 'r')
        self.canvas.draw()


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

