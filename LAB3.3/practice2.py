import wiringpi as wp
import time


LDR_PIN = 1
LED_PINS = [3, 4, 5, 6]

wp.wiringPiSetup()
for x in LED_PINS:
    wp.pinMode(x, 1)
wp.pinMode(LDR_PIN, 0)

def check_ldr():
    if wp.digitalRead(LDR_PIN):  # Hoog signaal (licht aanwezig)
        wp.digitalWrite(LED_PINS[0], 0)
        wp.digitalWrite(LED_PINS[1], 0)
        wp.digitalWrite(LED_PINS[2], 0)
        wp.digitalWrite(LED_PINS[3], 0)

        print("Light OFF")
    else:  # Laag signaal (geen licht)
        wp.digitalWrite(LED_PINS[0], 1)
        wp.digitalWrite(LED_PINS[1], 1)
        wp.digitalWrite(LED_PINS[2], 1)
        wp.digitalWrite(LED_PINS[3], 1)
        print("Light ON")

while True:
    check_ldr()
    time.sleep(0.5)
