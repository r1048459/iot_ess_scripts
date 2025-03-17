import wiringpi
import time

LED_PIN = 2
PIN_SWITCH = 1


wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_PIN, 1)
wiringpi.pinMode(PIN_SWITCH, 0)



def short(LED_PIN):
    for i in range(0,3):
        wiringpi.digitalWrite(LED_PIN, 1)
        time.sleep(0.5)  

        wiringpi.digitalWrite(LED_PIN, 0)
        time.sleep(0.2)

def long(LED_PIN):
    for i in range(0,3):
        wiringpi.digitalWrite(LED_PIN, 1)
        time.sleep(1.5)  

        wiringpi.digitalWrite(LED_PIN, 0)
        time.sleep(0.2)

while True:
    if(wiringpi.digitalRead(PIN_SWITCH) == 1):
        short(LED_PIN)
        long(LED_PIN)
        short(LED_PIN)
    


        
