import wiringpi
import time

LED_PIN = 2

wiringpi.wiringPiSetup()
for x in LED_PIN:
    wiringpi.pinMode(x, 1)


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
    short(LED_PIN)
    long(LED_PIN)
    short(LED_PIN)

        
