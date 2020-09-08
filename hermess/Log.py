import threading
from datetime import datetime
import ctypes
import serial
import time
import logging


logger = logging.getLogger(__name__)


def start_stop_read(self):
    if not self.start_stop_read:
        lock = threading.Lock()
        thread = threading.Thread(target=read_data, args=(self,))
        thread.daemon = True
        running = True
        time_now = datetime.now()
        save = open("log/{}".format(time_now.strftime('%Y%m%d-%H%M%S')), "w+")
        self.threadReadPackage = [lock, thread, running, save]
        self.start_stop_read = True

        thread_plot = threading.Thread(target=update_plot, args=(self,))
        thread_plot.daemon = True
        running_plot = True
        self.plotted = True
        self.threadPlotPackage = [lock, thread_plot, running_plot]

        self.threadReadPackage[1].start()
        self.threadPlotPackage[1].start()
    else:
        self.start_stop_read = False
        self.threadReadPackage[0].acquire()
        self.threadReadPackage[2] = False
        self.threadReadPackage[0].release()
        self.threadPlotPackage[0].acquire()
        self.threadPlotPackage[2] = False
        self.threadPlotPackage[0].release()


def read_data(self):
    running = True
    ser = serial.Serial(self.port, 19200, stopbits=1, parity=serial.PARITY_NONE)
    ser.close()
    ser.open()
    ser.write(b'\xFF')
    logger.info('Starting byte sent')
    # TODO: os.remove(self.threadReadPackage[3].name)

    while running:
        self.threadReadPackage[0].acquire()
        running = self.threadReadPackage[2]
        self.threadReadPackage[0].release()
        # TODO LIST com ports in combo box
        # TODO autosave

        get_val = list(ser.read(3))
        if get_val[2] != 255:
            logger.warning("Not proper control value: " + str(get_val))
        val = ctypes.c_int16((get_val[0] << 8) | get_val[1]).value

        self.threadReadPackage[3].write("%d\t\t%s\n" % (val, datetime.now()))
        self.threadReadPackage[0].acquire()
        self.allData.append(val)
        self.threadReadPackage[0].release()

    if running:
        ser.close()
    self.threadReadPackage[3].close()


def update_plot(self):
    running = True
    data = self.allData

    while running:
        self.threadPlotPackage[0].acquire()
        running = self.threadPlotPackage[2]
        self.threadPlotPackage[0].release()

        if len(data) > 0:
            self.dms_01Label.setText(str(data[-1]))

        self.canvas.axes.cla()
        self.canvas.axes.plot(data, 'r')
        self.canvas.draw()
        time.sleep(0.04)
