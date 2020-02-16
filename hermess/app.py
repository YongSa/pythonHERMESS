import sys
import time
from hermess import log, plot
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from tabulate import tabulate

"""
ToDo
    - offset (38, 76), startadresse auf GUI eingeben
    - lb sowie hb eingebbar (station address), ID für einzelne brücken sowie für insgesamt (667)
    - speichern von confi
"""
#floatfmt=".16f"; zur Zeit floats abgeschnitten
#was schnelleres als tabulate benutzen (strings/list to csv)
#Graphisch Darstellen?
#convert nimmt auch nur Format 64 LEERZEILE 08, kein 6408, kein 64,08, was wenn 5 werte rauskommen -> Fehler!
#dmsdat[i/2] = ddat[i/2]*messber[i/2]/0.065536/((1.0+nue[i/2])/4*kfakt[i/2])/uspeise[i/2];
"""
if (read_adc > 0) {
    adc_fd = open("/sys/bus/iio/devices/iio:device0/in_voltage1_raw", O_RDONLY);
    read(adc_fd, &adcval, 5);
    fadcval = (atof(adcval)-adc_zero)*1.8/4095.0*adc_cal;
    close(adc_fd);
    0,1575 = (2639 - 2615)*1,8/4095*14,927 -> 2639mV ... 2,639V

    for (i=0; i<8; i++) {
       kfakt[i]   = 2.0;
       uspeise[i] = 2.5;
       messber[i] = .005;
       nue[i]     = 0.3;
          fprintf(stderr,"\nMessbereich:         ");
for (i=0; i<8; i++) {fprintf(stderr,"%8.4f",messber[i]); messber[i] = 2.*messber[i];}
fprintf(stderr,"\nSpeisespannung:      ");
for (i=0; i<8; i++) {fprintf(stderr,"%8.4f",uspeise[i]);}
fprintf(stderr,"\nk-Faktor DMS:        ");
for (i=0; i<8; i++) {fprintf(stderr,"%8.4f",kfakt[i]);}
fprintf(stderr,"\nQuerkontraktion nue: ");
for (i=0; i<8; i++) {fprintf(stderr,"%8.4f",nue[i]);}
"""
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
        self.testPlotButton.clicked.connect(self.test_plot)
        self.setSR_DMSButton.clicked.connect(self.setSR_DMS)
        self.setSR_TEMPButton.clicked.connect(self.setSR_TEMP)
        self.setFF_DMSButton.clicked.connect(self.setFF_DMS)
        self.tareButton.clicked.connect(self.tare)

    def start_logging(self):
        log.setup(self)

    def stop_logging(self):
        log.stop()

    def save_results(self):
        try:
            save = open("log/" + time.strftime("%Y%m%d-%H%M%S") + ".txt","w")
            save.write(tabulate(log.getTable(), headers=["TIME","CAN_ID", "CAN_DATA", "1", "2", "3", "4"], tablefmt="tsv", missingval="?"))
            save.close()
            log.emptyTable()
        except:
            print("Wasn't able to save!")

    def test_plot(self):
        plot.plotTest("test3.txt")

    def setSR_DMS(self):
        log.setSRFF(0x667, 0xEA, 0x0E, 0x26, self.dmsSRCombo.currentIndex()) #Index 0 stimmt eventuell nicht, kein 1Hz

    def setSR_TEMP(self):
        log.setSRFF(0x667, 0xA2, 0x0C, 0x26, self.tempSRCombo.currentIndex())#Index 0 stimmt eventuell nicht, kein 1Hz

    def setFF_DMS(self):
        log.setSRFF(0x667, 0xEA, 0x0E, 0x28, ((self.dmsFFCombo.currentIndex()+1*self.dmsFFCombo.currentIndex()+1)*2)) #Index anscheinend kein Indikator (-> 1 2, 2 8, 3 18 ...) für Filter*2

    def tare(self):
        log.tare(0x667,0xEA,0x0E)
        log.tare(0x667,0xA2,0x0C)

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

