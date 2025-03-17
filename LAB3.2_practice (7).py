import wiringpi as wp
import time

# Gebruik WiringPi pin-nummers, NIET fysieke pinnen
IN1 = 5   # Fysieke pin 11 (GPIO 120)
IN2 = 6   # Fysieke pin 12 (GPIO 114)
IN3 = 7   # Fysieke pin 13 (GPIO 119)
IN4 = 8   # Fysieke pin 15 (GPIO 362)

# Stap-sequentie voor de 28BYJ-48 stepper motor
sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Init WiringPi
wp.wiringPiSetup()

# Stel de GPIO-pinnen in als output
for pin in (IN1, IN2, IN3, IN4):
    wp.pinMode(pin, 1)  # 1 = output
    wp.digitalWrite(pin, 0)

def stepper_motor(steps, delay=0.010):
    """ Laat de stappenmotor een aantal stappen draaien """
    step_count = len(sequence)

    if steps < 0:
        steps = -steps
        direction = -1
    else:
        direction = 1

    for _ in range(steps):
        for step in range(step_count)[::direction]:  # Vooruit of achteruit
            wp.digitalWrite(IN1, sequence[step][0])
            wp.digitalWrite(IN2, sequence[step][1])
            wp.digitalWrite(IN3, sequence[step][2])
            wp.digitalWrite(IN4, sequence[step][3])
            time.sleep(delay)

try:
    print("Stepper motor draait vooruit...")
    stepper_motor(200)  # 512 stappen = ongeveer 1 rotatie
    time.sleep(1)

    print("Stepper motor draait achteruit...")
    stepper_motor(-200)  # Draait terug

except KeyboardInterrupt:
    print("Gestopt door gebruiker.")

finally:
    print("GPIO opruimen...")
    for pin in (IN1, IN2, IN3, IN4):
        wp.digitalWrite(pin, 0)
