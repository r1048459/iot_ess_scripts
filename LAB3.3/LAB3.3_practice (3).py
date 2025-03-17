import wiringpi as wp
import time

LDR_PIN = 1
LED_PINS = [3, 4, 5, 6]
SWITCH_PIN = 2  # Change if needed

# GPIO setup
wp.wiringPiSetup()
for x in LED_PINS:
    wp.pinMode(x, 1)  # Set LED pins as output
wp.pinMode(LDR_PIN, 0)  # Set LDR as input
wp.pinMode(SWITCH_PIN, 0)  # Set switch as input

def check_ldr():
    ldr_state = wp.digitalRead(LDR_PIN)
    switch_state = wp.digitalRead(SWITCH_PIN)

    if (ldr_state == 0) or (switch_state == 0):  # Lights ON if dark OR switch pressed
        for led in LED_PINS:
            wp.digitalWrite(led, 1)  # Turn LEDs ON
        print("Light ON")
    else:
        for led in LED_PINS:
            wp.digitalWrite(led, 0)  # Turn LEDs OFF
        print("Light OFF")

while True:
    check_ldr()
    time.sleep(0.5)

