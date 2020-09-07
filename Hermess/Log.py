import threading
import time

import ctypes
import serial

# def updatePlot(self):
#     running = True
#     while running == True:
#         self.canvas.axes.cla()
#         # Adds data
#         generateData(self)
#
#         selectedGraph = int(self.dmsChooser.value()) - 1
#         self.canvas.axes.plot(self.ydata[0][selectedGraph], 'r')
#         self.canvas.draw()
#         self.threadPackage[0].acquire()
#         running = self.threadPackage[2]
#         self.threadPackage[0].release()
#         time.sleep(0.01)
#     self.threadPackage[5].close()
#
# def startLog(self):
#     lock = threading.Lock()
#     thread = threading.Thread(target=updatePlot, args=(self,))
#     thread.daemon = True
#     running = True
#     self.plotted = True
#     force = open("log/20200212-135138.txt", 'r')
#     temp = open("log/20200214-180026.txt", 'r')
#     dataSt = [[], [], [], [], [], []]
#     tempSt = [[], [], []]
#     self.allData = [copy.deepcopy(dataSt), copy.deepcopy(tempSt), copy.deepcopy(dataSt), copy.deepcopy(tempSt), []]
#     timeNow = time.localtime(time.time())
#     save = open("log/%s%02d%02d-%02d%02d%02d.txt" % (timeNow.tm_year, timeNow.tm_mon, timeNow.tm_mday, timeNow.tm_hour, timeNow.tm_min, timeNow.tm_sec), "w+")
#     self.threadPackage = [lock, thread, running, force, temp, save]
#     self.threadPackage[1].start()
#
# def stopLog(self):
#     if self.threadPackage[2] == True:
#         self.threadPackage[0].acquire()
#         self.threadPackage[2] = False
#         self.threadPackage[0].release()
#     else:
#         print("Not running the logger, why stopping it then")
#
# def generateData(self):
#     if self.threadPackage[3].closed == True:
#         self.threadPackage[3] = open("log/20200212-135138.txt", 'r')
#     if self.threadPackage[4].closed == True:
#         self.threadPackage[4] = open("log/20200214-180026.txt", 'r')
#
#     forceDataOne = self.threadPackage[3].readline().split()
#     if self.threadPackage[3].closed == True:
#         self.threadPackage[3] = open("log/20200212-135138.txt", 'r')
#     forceDataTwo = self.threadPackage[3].readline().split()
#     tempData = self.threadPackage[4].readline().split()
#
#
#     force1 = float(forceDataOne[10])
#     force2 = float(forceDataOne[11])
#     force3 = float(forceDataOne[12])
#     force4 = float(forceDataTwo[10])
#     force5 = float(forceDataOne[11])
#     force6 = float(forceDataOne[12])
#     temp1 = float(tempData[10])
#     temp2 = float(tempData[11])
#     temp3 = float(tempData[12])
#
#     self.dms_01Label.setText(str(force1))
#     self.dms_02Label.setText(str(force2))
#     self.dms_03Label.setText(str(force3))
#     self.dms_04Label.setText(str(force4))
#     self.dms_05Label.setText(str(force5))
#     self.dms_06Label.setText(str(force6))
#
#     self.temp_01Label.setText(str(temp1))
#     self.temp_02Label.setText(str(temp2))
#     self.temp_03Label.setText(str(temp3))
#
#     timeNow = time.time()
#
#     if len(self.ydata[0][0]) < 100:
#         self.ydata[0][0] = self.ydata[0][0] + [force1]
#         self.ydata[0][1] = self.ydata[0][1] + [force2]
#         self.ydata[0][2] = self.ydata[0][2] + [force3]
#         self.ydata[0][3] = self.ydata[0][3] + [force4]
#         self.ydata[0][4] = self.ydata[0][4] + [force5]
#         self.ydata[0][5] = self.ydata[0][5] + [force6]
#
#         self.ydata[1][0] = self.ydata[1][0] + [temp1]
#         self.ydata[1][1] = self.ydata[1][1] + [temp2]
#         self.ydata[1][2] = self.ydata[1][1] + [temp3]
#
#         self.ydata[2] = self.ydata[1] + [timeNow]
#     # Continous writing
#     else:
#         self.ydata[0][0] = self.ydata[0][0][1:] + [force1]
#         self.ydata[0][1] = self.ydata[0][1][1:] + [force2]
#         self.ydata[0][2] = self.ydata[0][2][1:] + [force3]
#         self.ydata[0][3] = self.ydata[0][3][1:] + [force4]
#         self.ydata[0][4] = self.ydata[0][4][1:] + [force5]
#         self.ydata[0][5] = self.ydata[0][5][1:] + [force6]
#
#         self.ydata[1][0] = self.ydata[1][0][1:] + [temp1]
#         self.ydata[1][1] = self.ydata[1][1][1:] + [temp2]
#         self.ydata[1][2] = self.ydata[1][1][1:] + [temp3]
#
#     self.ydata[2] = self.ydata[1][1:] + [timeNow]
#
#     string = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (force1, force2, force3, force4, force5, force6,
#                                                            temp1, temp2, temp3, timeNow)
#     self.threadPackage[5].write(string)

def startStopRead(self):
    if self.startStopRead == False:
        lock = threading.Lock()
        thread = threading.Thread(target=readData, args=(self,))
        thread.daemon = True
        running = True
        timeNow = time.localtime(time.time())
        save = open("log/%s%02d%02d-%02d%02d%02d.txt" % (timeNow.tm_year, timeNow.tm_mon, timeNow.tm_mday, timeNow.tm_hour, timeNow.tm_min, timeNow.tm_sec), "w+")
        self.threadReadPackage = [lock, thread, running, save]
        self.startStopRead = True

        threadPlot = threading.Thread(target=updatePlot, args=(self,))
        threadPlot.daemon = True
        runningPlot = True
        self.plotted = True
        self.threadPlotPackage = [lock, threadPlot, runningPlot]

        self.threadReadPackage[1].start()
        self.threadPlotPackage[1].start()
    else:
        self.startStopRead = False
        self.threadReadPackage[0].acquire()
        self.threadReadPackage[2] = False
        self.threadReadPackage[0].release()
        self.threadPlotPackage[0].acquire()
        self.threadPlotPackage[2] = False
        self.threadPlotPackage[0].release()

def readData(self):
    running = True
    try:
        ser = serial.Serial(self.port, 19200, stopbits=1, parity=serial.PARITY_NONE)
        ser.close()
        ser.open()
    except:
        startStopRead(self)
        #TODO: os.remove(self.threadReadPackage[3].name)

    while running == True:
        self.threadReadPackage[0].acquire()
        running = self.threadReadPackage[2]
        self.threadReadPackage[0].release()
        try:
            # TODO
            # LIST com ports in combo box
            # autosave

            getVal = ser.read_until(b'\xff')
            listTestByte = list(getVal)
            testVal = ctypes.c_int16((listTestByte[0] << 8) | listTestByte[1]).value
            print(testVal)
            
            val = testVal #int(getVal)
            self.threadReadPackage[3].write("%d\t\t%s\n" % (val, time.localtime(time.time())))
            self.threadReadPackage[0].acquire()
            self.allData.append(val)
            self.threadReadPackage[0].release()
        except:
            print("Keyboard Interrupt")
            raise

    ser.close()
    self.threadReadPackage[3].close()

def updatePlot(self):
    running = True
    data = self.allData

    while running == True:
        self.threadPlotPackage[0].acquire()
        running = self.threadPlotPackage[2]
        self.threadPlotPackage[0].release()

        if len(data) > 0:
            self.dms_01Label.setText(str(data[-1]))

        self.canvas.axes.cla()
        self.canvas.axes.plot(data, 'r')
        self.canvas.draw()
        time.sleep(0.04)
