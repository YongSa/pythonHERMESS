import random
import threading
import time

def updatePlot(self):
    running = self.threadPackage[2]
    while running == True:
        self.canvas.axes.cla()
        # Adds data
        generateData(self)

        self.canvas.axes.plot(self.ydata[0][0], 'r')
        self.canvas.draw()
        self.threadPackage[0].acquire()
        running = self.threadPackage[2]
        self.threadPackage[0].release()
        time.sleep(0.01)

def startLog(self):
    lock = threading.Lock()
    thread = threading.Thread(target=updatePlot, args=(self,))
    thread.daemon = True
    running = True
    force = open("log/20200212-135138.txt", 'r')
    temp = open("log/20200214-180026.txt", 'r')
    self.threadPackage = [lock, thread, running, force, temp]
    self.threadPackage[1].start()

def stopLog(self):
    if self.threadPackage[2] == True:
        self.threadPackage[0].acquire()
        self.threadPackage[2] = False
        self.threadPackage[0].release()
    else:
        print("Not running the logger, why stopping it then")

def generateData(self):
    if self.threadPackage[3].closed == True:
        self.threadPackage[3] = open("log/20200212-135138.txt", 'r')
    if self.threadPackage[4].closed == True:
        self.threadPackage[4] = open("log/20200214-180026.txt", 'r')

    forceDataOne = self.threadPackage[3].readline().split()
    if self.threadPackage[3].closed == True:
        self.threadPackage[3] = open("log/20200212-135138.txt", 'r')
    forceDataTwo = self.threadPackage[3].readline().split()
    tempData = self.threadPackage[4].readline().split()


    force1 = float(forceDataOne[10])
    force2 = float(forceDataOne[11])
    force3 = float(forceDataOne[12])
    force4 = float(forceDataTwo[10])
    force5 = float(forceDataOne[11])
    force6 = float(forceDataOne[12])
    temp1 = float(tempData[10])
    temp2 = float(tempData[11])
    temp3 = float(tempData[12])

    if len(self.ydata[0][0]) < 100:
        self.ydata[0][0] = self.ydata[0][0] + [force1]
        self.ydata[0][1] = self.ydata[0][1] + [force2]
        self.ydata[0][2] = self.ydata[0][2] + [force3]
        self.ydata[0][3] = self.ydata[0][3] + [force4]
        self.ydata[0][4] = self.ydata[0][4] + [force5]
        self.ydata[0][5] = self.ydata[0][5] + [force6]

        self.ydata[1][0] = self.ydata[1][0] + [temp1]
        self.ydata[1][1] = self.ydata[1][1] + [temp2]
        self.ydata[1][2] = self.ydata[1][1] + [temp3]

        self.ydata[2] = self.ydata[1] + [time.time()]
    # Continous writing
    else:
        self.ydata[0][0] = self.ydata[0][0][1:] + [force1]
        self.ydata[0][1] = self.ydata[0][1][1:] + [force2]
        self.ydata[0][2] = self.ydata[0][2][1:] + [force3]
        self.ydata[0][3] = self.ydata[0][3][1:] + [force4]
        self.ydata[0][4] = self.ydata[0][4][1:] + [force5]
        self.ydata[0][5] = self.ydata[0][5][1:] + [force6]

        self.ydata[1][0] = self.ydata[1][0][1:] + [temp1]
        self.ydata[1][1] = self.ydata[1][1][1:] + [temp2]
        self.ydata[1][2] = self.ydata[1][1][1:] + [temp3]

    self.ydata[2] = self.ydata[1][1:] + [time.time()]
