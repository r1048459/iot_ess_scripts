import wiringpi
import time

LED_PIN = [2, 3, 4, 6]  

wiringpi.wiringPiSetup()
for x in LED_PIN:
    wiringpi.pinMode(x, 1)

while True:
    for pin in LED_PIN:
        wiringpi.digitalWrite(pin, 1)
        time.sleep(0.1)  

    for pin in LED_PIN:
        wiringpi.digitalWrite(pin, 0)  
        time.sleep(0.1)  
