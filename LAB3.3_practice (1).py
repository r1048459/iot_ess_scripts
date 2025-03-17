import wiringpi as wp
import time


LDR_PIN = 1

wp.wiringPiSetup()
wp.pinMode(LDR_PIN, 0)

def check_ldr():
    if wp.digitalRead(LDR_PIN):  # Hoog signaal (licht aanwezig)
        print("Licht gedetecteerd - GPIO1 is HIGH")
    else:  # Laag signaal (geen licht)
        print("Geen licht - GPIO1 is LOW")

while True:
    check_ldr()
    time.sleep(1)  # Wacht 1 seconde voordat de volgende meting plaatsvindt
