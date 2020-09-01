#The connection uses a baud rate of 9600 baud. One transmission consists of 8 data bits and one parity bit. 
#Here, odd parity is used. After 30 transmissions the MCU checks whether the workstation is still receiving and has not encountered any errors.  
#During this check, a cyclic redundancy check is used to provide a more secure data validation.
#The 8th bit in each transmission is used to escape all data transmissions from the command codes. 
#This results in all command codes ending with a 1, and all data transmissions with a zero. This way, the 7th data bit represents the MSB and the first bit the LSB.
#In the case that a STILL_AWAKE command is answered by a DATA_ERR command, the MCU will interpret this as an error in data transmission and will resend all data since the last confirmed correct transmission. 
#This process will repeat until the packet of 30 transmissions is received correctly.
#The same procedure will also be used if an EOF command is answered by DATA_ERR command. In this case the amount of repeated data transmissions may be less than 30.
#All the configuration commands and the RESET command will be waiting for an ACKNOWLEDGED command from the MCU. If this ACKNOWLEDGED command is not received after a timeout, the command is sent again.

#Command code   Command name	Description
#0x01	        READ_ALL	    request for sending all available data
#0x03	        ACKNOWLEDGED	positive answer
#0x05	        STILL_AWAKE	    check, if workstation is still listening
#0x07	        EOF	            end of file
#0x09	        DATA_ERR	    error in parity bit, or CRC, can be an answer to STILL_AWAKE or EOT results in all the data transmissions since the last check, being sent again
#0x0B	        Placeholder for configuration command	placeholder for configuration command
#0x0D	        Placeholder for configuration command	placeholder for configuration command
#0x0F	        Placeholder for configuration command	placeholder for configuration command
#0x11	        Placeholder for configuration command	placeholder for configuration command
#0x13	        Placeholder for configuration command	placeholder for configuration command
#0x15	        RESET	        used for resetting the MCU

import struct

# a Serial class emulator 
class Serial:

    def __init__( self, port = 'COM1', baudrate = 9600, timeout = 0,
                  bytesize = 8, parity = 'O', stopbits = 1, xonxoff = 0,
                  rtscts = 0):
        self.name     = 'Hermess'
        self.port     = port
        self.timeout  = timeout
        self.parity   = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff  = xonxoff
        self.rtscts   = rtscts
        self._isOpen  = True
        self._receivedData = ""
        self._data = ""
        
    ## isOpen()
    # returns True if the port is open.  False otherwise
    def isOpen( self ):
        return self._isOpen

    ## open()
    # opens the port
    def open( self ):
        self._isOpen = True
        self._data += str(struct.pack("B", 255))
        print(self._data)

    ## close()
    # closes the port
    def close( self ):
        self._isOpen = False
        
    ## read()
    def read( self, n=1 ):
        s = self._data[0:n]
        self._data = self._data[n:]
        return s

    ## readline()
    #def readline( self ):
    #    returnIndex = self._data.index( "\n" )
    #    if returnIndex != -1:
    #        s = self._data[0:returnIndex+1]
    #        self._data = self._data[returnIndex+1:]
    #        return s
    #    else:
    #        return ""
            
    ## write()
    def write( self, string ):
        print(string + ' ACKNOWLEDGED' )
        self._receivedData += string

    def READ_ALL( self, n = 8 ):
        self.write('READ_ALL')
        if (len(self._data) >= 8):
            return self.read(n)
        elif (len(self._data) >= 1):
            return self.read(len(self._data)) + "\n" + 'EOL'
        else:
            return 'EOL'
     
    def STILL_AWAKE( self ):
        self.write('STILL_AWAKE')
        print(self.isOpen())
        return self.isOpen()

    def RESET( self ):
        self.write('RESET')
        self.close()
        self.open()

    ## __str__()
    # returns a string representation of the serial class
    def __str__( self ):
        return  "Serial<id=0xa81c10, open=%s>( port='%s', baudrate=%d," \
               % ( str(self.isOpen), self.port, self.baudrate ) \
               + " bytesize=%d, parity='%s', stopbits=%d, xonxoff=%d, rtscts=%d)"\
               % ( self.bytesize, self.parity, self.stopbits, self.xonxoff,
                   self.rtscts )