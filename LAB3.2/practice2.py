import wiringpi
import time

LED_PIN = 2
PIN_SWITCH = 1

wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_PIN, 1)
wiringpi.pinMode(PIN_SWITCH, 0)

while True:
    if(wiringpi.digitalRead(PIN_SWITCH) == 0):
        print("LED blinks")
        time.sleep(0.3)
        wiringpi.digitalWrite(LED_PIN, 1)
        time.sleep(0.5)  
        wiringpi.digitalWrite(LED_PIN, 0)
        time.sleep(0.5)
    else:
        print("LED not flashing")
        time.sleep(0.3)
        wiringpi.digitalWrite(LED_PIN, 0)