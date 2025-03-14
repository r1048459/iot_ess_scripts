import wiringpi
import time

LED_PIN = [2, 3, 4, 6]

wiringpi.wiringPiSetup()
for x in LED_PIN:
    wiringpi.pinMode(x, 1)

while True:
    wiringpi.digitalWrite(LED_PIN[0], 1)
    wiringpi.digitalWrite(LED_PIN[1], 1)
    wiringpi.digitalWrite(LED_PIN[2], 1)
    wiringpi.digitalWrite(LED_PIN[3], 1)  
    time.sleep(0.1)

    wiringpi.digitalWrite(LED_PIN[0], 0)
    wiringpi.digitalWrite(LED_PIN[1], 0)
    wiringpi.digitalWrite(LED_PIN[2], 0)
    wiringpi.digitalWrite(LED_PIN[3], 0) 
    time.sleep(0.1)