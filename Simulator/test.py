# testSerialSimulator.py
# D. Thiebaut
# This program energizes the fakeSerial simulator using example code taken
# from http://pyserial.sourceforge.net/shortintro.html
#

# import the simulator module (it should be in the same directory as this program)
import sim as serial

# Example 1  from http://pyserial.sourceforge.net/shortintro.html
def Example1():
    ser = serial.Serial(0)  # open first serial port
    #print( ser.name )       # check which port was really used
    #ser.write(STILL_AWAKE)      # write a string
    ser.open()
    print(ser.READ_ALL())
    ser.close()             # close port

# Example 2  from http://pyserial.sourceforge.net/shortintro.html
#def Example2():
#    ser = serial.Serial('/dev/ttyS1', 19200, timeout=1)
#    x = ser.read()          # read one byte
#    print( "x = ", x )
#    s = ser.read(10)        # read up to ten bytes (timeout)
#    print( "s = ", s )
#    line = ser.readline()   # read a '\n' terminated line
#    ser.close()
#    print( "line = ", line )

# Example 3  from http://pyserial.sourceforge.net/shortintro.html
#def Example3():
#    ser = serial.Serial()
#    ser.baudrate = 19200
#    ser.port = 0
#    print( ser )
#    
#    ser.open()
#    print( str( ser.isOpen() ) )
#
#   ser.close()
#    print( ser.isOpen() )
    

Example1()
#Example2()
#Example3()