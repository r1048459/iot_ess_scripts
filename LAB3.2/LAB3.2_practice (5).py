import wiringpi
import time

LED_PIN = [2, 3, 4, 5] 
PIN_SWITCH = 1 

wiringpi.wiringPiSetup()
for x in LED_PIN:
    wiringpi.pinMode(x, 1)
wiringpi.pinMode(PIN_SWITCH, 1)

while True:
    if(wiringpi.digitalRead(PIN_SWITCH) == 1):
        for pin in LED_PIN:
            wiringpi.digitalWrite(pin, 1)
            time.sleep(0.1)
            wiringpi.digitalWrite(pin, 0)  
    else:
        for pin in reversed(LED_PIN):
            wiringpi.digitalWrite(pin, 1)
            time.sleep(0.1)
            wiringpi.digitalWrite(pin, 0)
