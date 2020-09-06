import random
import threading
import time

from PyQt5 import QtCore


def updatePlot(self):
    running = self.threadPackage[2]
    while running == True:
        self.canvas.axes.cla()
        # Adds data
        if len(self.ydata) < 200:
            self.ydata = self.ydata + [random.randint(0, 10)]
        # Continous writing
        else:
            self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.plot(self.ydata, 'r')
        self.canvas.draw()
        self.threadPackage[0].acquire()
        running = self.threadPackage[2]
        self.threadPackage[0].release()
        time.sleep(0.1)

def startLog(self):
    lock = threading.Lock()
    thread = threading.Thread(target=updatePlot, args=(self,))
    thread.daemon = True
    running = True
    self.threadPackage = [lock, thread, running]
    self.threadPackage[1].start()

def stopLog(self):
    self.threadPackage[0].acquire()
    self.threadPackage[2] = False
    self.threadPackage[0].release()
