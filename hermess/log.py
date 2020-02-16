import can
from hermess import convert as conv

table= []

def getTable():
    return table

def emptyTable():
    table.clear()

def setup(obj):
    global GUI
    global bus
    global notifier
    GUI= obj
    try:
        bus= can.Bus(interface= GUI.canInterfaceCombo.currentText(),
                      channel= GUI.canChannelCombo.currentText(),
                      bitrate= GUI.canBitrateCombo.currentText())
        notifier= can.Notifier(bus, [receive])
    except:
        setup(obj) # sollte geändert werden

def stop():
    try:
        notifier.stop()
        bus.shutdown()
    except:
        print("There is no bus or notifier to stop.")

def receive(msg):
    if GUI.absStrainCheck.isChecked():
        table.append(conv.convertAbs(msg.timestamp, msg.arbitration_id, list(msg.data), float(GUI.supVoltageEdit.text()), float(GUI.kFactorEdit.text()), float(GUI.latStrainEdit.text()), 2.0*float(GUI.meRangeEdit.text())))
    else:
        table.append(conv.convert(msg.timestamp, msg.arbitration_id, list(msg.data)))
    if GUI.outputCheck.isChecked():
        print(table[-1])
        if table[-1][1] == 100:
            GUI.dms_1Label.setText(str(table[-1][3]))
            GUI.dms_2Label.setText(str(table[-1][4]))
            GUI.dms_3Label.setText(str(table[-1][5]))
            GUI.dms_4Label.setText(str(table[-1][6]))
        elif table[-1][1] == 101:
            GUI.dms_5Label.setText(str(table[-1][3]))
            GUI.dms_6Label.setText(str(table[-1][4]))
            GUI.dms_7Label.setText(str(table[-1][5]))
            GUI.dms_8Label.setText(str(table[-1][6]))
        elif table[-1][1] == 102:
            GUI.temp_1Label.setText(str(table[-1][3]))
            GUI.temp_2Label.setText(str(table[-1][4]))
            GUI.temp_3Label.setText(str(table[-1][5]))
            GUI.temp_4Label.setText(str(table[-1][6]))
        elif table[-1][1] == 103:
            GUI.temp_5Label.setText(str(table[-1][3]))
            GUI.temp_6Label.setText(str(table[-1][4]))
            GUI.temp_7Label.setText(str(table[-1][5]))
            GUI.temp_8Label.setText(str(table[-1][6]))
    if GUI.saveCheck.isChecked():
        autoSave= open("log/autosave.txt","a")
        autoSave.write(str(table[-1]) + "\n")
        autoSave.close()

def tare(canID, lb, hb):
    sendToBus(canID, [0x1,0x1,lb,hb,0x00,0x00,0x00,0x00])
    sendToBus(canID, [0x02,0x02,0x00,0x00,0x03,0x1b,0x08,0x00])
    sendToBus(canID, [0x03,0x03,0x01,0x01,0x00,0x00,0x00,0x00])
    sendToBus(canID, [0x07,0x04,0x01,0x00,lb,hb,0x00,0x00])

def setSRFF(canID, lb, hb, offset, frequency):
    sendToBus(canID, [0x1,0x1,lb,hb,0x00,0x00,0x00,0x00])
    try:
        adr= 0x00081C00+offset
        for i in range(8):
            adr3= int(adr/0x10000/0x100)
            adr2= int((adr-adr3*0x10000*0x100)/0x10000)
            adr1= int((adr-adr3*0x10000*0x100-adr2*0x10000)/0x100)
            adr0= int(adr-adr3*0x10000*0x100-adr2*0x10000-adr1*0x100)
            sendToBus(canID, [0x02,0x02,0x00,0x00,adr0,adr1,adr2,adr3])
            sendToBus(canID, [0x03,0x03,0x01,frequency,0x00,0x00,0x00,0x00])
            adr= int(adr+0x4C)
    except:
        print("Something went wrong!")
    sendToBus(canID, [0x02,0x02,0x00,0x00,0x03,0x1b,0x08,0x00])
    sendToBus(canID, [0x03,0x03,0x01,0x01,0x00,0x00,0x00,0x00])
    sendToBus(canID, [0x07,0x04,0x01,0x00,lb,hb,0x00,0x00])

def sendToBus(canID, canData):
    try:
        bus.send(can.Message(arbitration_id= canID, data= canData, is_extended_id= False))
    except:
        print("Something went wrong!")
