#include <SPI.h>

#define PIN_RESET 9
#define PIN_START 8
#define PIN_CS 10
#define PIN_DRDY 2
#define PIN_MOSI 11
#define PIN_MISO 12
#define PIN_CLK 13

#define CMD_RESET 0x07
#define CMD_SDATAC 0x17
#define CMD_RDATAC 0x14
#define CMD_SYNC 0x04
#define CMD_SELFOCAL 0x62
#define CMD_SYSOCAL 0x60
#define CMD_SYSGCAL 0x61

uint8_t drdy = 0;
int16_t calVals[12];
uint8_t calCount = 0;

void isr_drdy () {
  drdy++;
}



/* Sends the command to the SPI interface and sets the CS line
*/
byte sendCommand (byte toSend) {
  digitalWrite(PIN_CS, LOW);
  byte returner = SPI.transfer(toSend);
  digitalWrite(PIN_CS, HIGH);
  return returner;
}



/* Sends the command and sets CS line. Use a buffer to also receive the values back. Count in bytes
*/
void sendCommand (byte *toSendAndReceive, uint8_t count) {
  digitalWrite(PIN_CS, LOW);
  SPI.transfer(toSendAndReceive, count);
  digitalWrite(PIN_CS, HIGH);
}



void setup() {
  // setup the UART connection
  Serial.begin(19200);
  // Serial.println("Start");

  // !RESET Pin must be high, so its not in reset mode
  pinMode(PIN_RESET, OUTPUT);
  digitalWrite(PIN_RESET, HIGH);
  // START Pin must be high 
  pinMode(PIN_START, OUTPUT);
  digitalWrite(PIN_START, HIGH);
  // !CS Pin must be high to reset SPI interface connection
  pinMode(PIN_CS, OUTPUT);
  digitalWrite(PIN_CS, HIGH);
  // initialize all other used pins
  pinMode(PIN_MISO, INPUT);
  pinMode(PIN_MOSI, OUTPUT);
  pinMode(PIN_CLK, OUTPUT);
  pinMode(PIN_DRDY, INPUT);

  // initialize the SPI and interrupt
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
  SPI.begin();
  attachInterrupt(digitalPinToInterrupt(PIN_DRDY), isr_drdy, FALLING);
  
  // wait 16ms to settle adc
  delay(16);

  // initialize the ADC by soft-resetting and stopping continous
  // readback mode to enable safe reading of registers
  sendCommand(CMD_RESET);
  delay(1); // wait for the ADC to be active again
  sendCommand(CMD_SDATAC);

  // write the and perform validity check
  byte wregBuffer[] = {
    0x42, // WREG operation with start register address 2
    0x01, // Update two registers
    0x30, // Always on and selected internal reference
    0x72 // PGA 64 and 20 SPS
  };
  sendCommand(wregBuffer, 4);
  byte rregBuffer[] = {0x22, 0x01, 0xFF, 0xFF};
  sendCommand(rregBuffer, 4);
  uint16_t rregVal = (((uint16_t) rregBuffer[2]) << 8) | rregBuffer[3];
  if (rregVal != 0x3072) {
    Serial.print("Incorrect register readback: ");
    Serial.println(rregVal, HEX);
    for (;;) {}
  }

  // system and self offset calibration
  drdy = 0;
  sendCommand(CMD_SYSOCAL);
  //while (!drdy) {} would be better, but arduino standard compiler optimizes it away
  delay(2000);
  drdy = 0;
  sendCommand(CMD_SELFOCAL);
  //while (!drdy) {}
  delay(2000);

  // enable continious read mode again
  sendCommand(CMD_RDATAC);
  
  // Serial.println("ADC initialization complete");
}



void loop() {
  if (drdy) {
    byte readBuffer[] = {0xFF, 0xFF};
    sendCommand(readBuffer, 2);
    int16_t val = (readBuffer[0] << 8) | readBuffer[1];

    if (calCount < 12) {
      calVals[calCount++] = val;
      if (calCount == 12) {
        int32_t sum = 0;
        for (uint8_t i = 0; i < 12; i++)
          sum += calVals[i];
        calVals[0] = sum / 12;
      }
    }
    else {
      // print out calibrated value
      int16_t calVal = val - calVals[0];
      //Serial.write(calVal >> 8);
      //Serial.write(calVal & 0xff);
      //Serial.write(0xff);
      Serial.println(val - calVals[0]);
    }

    // If it was too fast for Arduino display here
    if (drdy > 1)
      Serial.println("D");
    drdy = 0;
  }
}
