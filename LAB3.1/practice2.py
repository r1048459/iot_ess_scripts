import wiringpi
import time

LED_PIN = 2

wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_PIN, 1)

while True:
    wiringpi.digitalWrite(LED_PIN, 1)
    time.sleep(0.5)  
    wiringpi.digitalWrite(LED_PIN, 0)
    time.sleep(0.5) 