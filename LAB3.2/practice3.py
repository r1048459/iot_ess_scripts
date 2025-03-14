import wiringpi
import time

LED_PIN = 2
RELAY_PIN = 16
PIN_SWITCH = 1

wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_PIN, 1)
wiringpi.pinMode(PIN_SWITCH, 0)
wiringpi.pinMode(RELAY_PIN, 1)

while True:
    if(wiringpi.digitalRead(PIN_SWITCH) == 0):
        print("LED blinks")
        time.sleep(0.3)
        wiringpi.digitalWrite(LED_PIN, 1)
        time.sleep(0.5)  
        wiringpi.digitalWrite(LED_PIN, 0)
        time.sleep(0.5)
        wiringpi.digitalWrite(RELAY_PIN, 1)
    else:
        print("LED not flashing")
        time.sleep(0.3)
        wiringpi.digitalWrite(LED_PIN, 0)
        wiringpi.digitalWrite(RELAY_PIN, 0)
