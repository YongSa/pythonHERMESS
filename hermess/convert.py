def convert(timeStamp, canID, values):
    temp = []
    dms = []
    try:
        if canID == 100 or canID == 101:
            for i in range(0,8,2):
                tmp = values[i+1]*256+values[i]
                if tmp > 32768:
                    tmp-=65536
                dms.append(tmp)
            return [timeStamp, canID, values, dms[0], dms[1], dms[2], dms[3]]
        elif canID == 102 or canID == 103:
            for i in range(0,8,2):
                tmp = values[i+1]*256+values[i]
                temp.append(tmp/65536.0*500.0-50.0)
            return [timeStamp, canID, values, temp[0], temp[1], temp[2], temp[3]]
        else:
            return [timeStamp, canID, values, 0, 0, 0, 0] #liebe als print vlt, damit nicht aus daten gelöscht werden muss
    except:
        print("Something went wrong!")
        return [0.0, 0, [], 0, 0, 0, 0]

def convertAbs(timeStamp, canID, values, supplyVoltage, kFactor, lateralStrain, measuringRange):
    temp = []
    dms = []
    try:
        if canID == 100 or canID == 101:
            for i in range(0,8,2):
                tmp = values[i+1]*256+values[i]
                if tmp > 32768:
                    tmp-=65536
                tmp= tmp*measuringRange/0.065536/((1.0+lateralStrain)/4*kFactor)/supplyVoltage
                dms.append(tmp)
            return [timeStamp, canID, values, dms[0], dms[1], dms[2], dms[3]]
        elif canID == 102 or canID == 103:
            for i in range(0,8,2):
                tmp = values[i+1]*256+values[i]
                temp.append(tmp/65536.0*500.0-50.0)
            return [timeStamp, canID, values, temp[0], temp[1], temp[2], temp[3]]
        else:
            return [timeStamp, canID, values, 0, 0, 0, 0] #liebe als print vlt, damit nicht aus daten gelöscht werden muss
    except:
        print("Something went wrong!")
        return [0.0, 0, [], 0, 0, 0, 0]

"""
def convertHEX(values): 
    values = values.split(" ")
    temp = []
    dms = []
    canID = values[0]
    del values[:2]
    values[:4],values[4:] = values[4:],values[:4]
    if canID == 100 or canID == 101:
        for i in range(0,8,2):
            tmp = int(values[i+1], base=16)*256 + int(values[i], base=16)
            if tmp > 32768:
                tmp-=65536
            dms.append(tmp)
            #plot.read([canID, int(i/2), dms[-1]])
        return [canID, values, dms[0], dms[1], dms[2], dms[3]]
    elif canID == 102 or canID == 103:
        for i in range(0,8,2):
            tmp = int(values[i+1], base=16)*256 + int(values[i], base=16)
            temp.append(tmp/65536.0*500.0-50.0)
            #plot.read([canID, int(i/2), temp[-1]])
        return [canID, values, temp[0], temp[1], temp[2], temp[3]]
    #else return???? 
"""
