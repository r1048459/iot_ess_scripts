import wiringpi
import time

PIN_SWITCH1 = 1
PIN_SWITCH2 = 2
PIN_RELAY1 = 3
PIN_RELAY2 = 4 


wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN_SWITCH1,0)
wiringpi.pinMode(PIN_SWITCH2,0)
wiringpi.pinMode(PIN_RELAY1, 1)
wiringpi.pinMode(PIN_RELAY2, 1)


while True:
    if(wiringpi.digitalRead(PIN_SWITCH1) == 1):
        wiringpi.digitalWrite(PIN_RELAY2, 1)
        wiringpi.digitalWrite(PIN_RELAY1, 0)
    if(wiringpi.digitalRead(PIN_SWITCH2) == 1):
        wiringpi.digitalWrite(PIN_RELAY1, 1)
        wiringpi.digitalWrite(PIN_RELAY2, 0)