import OPi.GPIO as GPIO
import smbus2
import time
import paho.mqtt.client as mqtt

# GPIO-pinnen
STEPPER_PINS = [13, 14, 15, 16]  # Stepper motor pinnen
LED_PIN = 2                       # LED pin
SWITCH_PIN = 3                    # Switch pin

# I2C-instellingen
I2C_BUS = 0                       # I2C-bus (0 voor Orange Pi)
BMP280_ADDR = 0x77                # BMP280 I2C-adres
BH1750_ADDR = 0x23                # BH1750 I2C-adres

# ThingSpeak MQTT-instellingen
MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_USERNAME = "EAEWESgCDS8kPTAYFjkLERk"
MQTT_PASSWORD = "0c/35VFsF8CJUw3nqMlaSCPv"
MQTT_CLIENT_ID = "EAEWESgCDS8kPTAYFjkLERk"
MQTT_TOPIC = "channels/2884475/publish"

# Initialisatie van GPIO
GPIO.setmode(GPIO.BOARD)          # Gebruik fysieke pin nummering
for pin in STEPPER_PINS:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SWITCH_PIN, GPIO.IN)   # Geen pull-up weerstand

# Initialisatie van I2C
bus = smbus2.SMBus(I2C_BUS)

# Stepper motor stappen (volgorde voor een 4-fase stepper motor)
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Functie om de stepper motor te draaien
def step_motor(steps, direction=1):
    for _ in range(steps):
        for step in STEP_SEQUENCE[::direction]:
            for pin, value in zip(STEPPER_PINS, step):
                GPIO.write(pin, value)
            time.sleep(0.01)

# Functie om de stepper motor te resetten
def reset_motor():
    step_motor(50, direction=-1)  # Draai terug naar de beginpositie

# Functie om de lux-waarde te lezen van de BH1750
def read_bh1750():
    bus.write_byte(BH1750_ADDR, 0x10)  # Continu meetmodus, 1 lux resolutie
    bytes_read = bus.read_i2c_block_data(BH1750_ADDR, 0x10, 2)
    return ((bytes_read[0] << 8) + bytes_read[1]) / 1.2

# Functie om de temperatuur te lezen van de BMP280
def read_bmp280():
    # BMP280 uitlezen zonder calibration_params
    data = bus.read_i2c_block_data(BMP280_ADDR, 0xFA, 6)
    temp_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp = (temp_raw / 16 - 27315) / 100  # Omrekenen naar graden Celsius
    return temp

# Functie om data naar ThingSpeak te sturen via MQTT
def send_to_thingspeak(temp, lux):
    payload = f"field1={temp}&field2={lux}"
    try:
        client.publish(MQTT_TOPIC, payload)
        print(f"ThingSpeak Data Sent: {payload}")
    except Exception as e:
        print(f"ThingSpeak MQTT Error: {e}")

# MQTT-client initialiseren
client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Hoofdprogramma
try:
    while True:
        # Lees de sensoren
        lux = read_bh1750()
        temp = read_bmp280()

        # Publiceer de sensorwaarden naar ThingSpeak
        send_to_thingspeak(temp, lux)

        # Controleer de lux-waarde en temperatuur
        if lux > 22:  # Als de lux-waarde hoger is dan 22
            step_motor(50)  # Draai de stepper motor
        elif temp < 20:  # Als de temperatuur lager is dan 20°C
            reset_motor()  # Reset de stepper motor

        # Controleer de switch
        if GPIO.read(SWITCH_PIN) == GPIO.LOW:  # Als de switch is ingedrukt
            GPIO.write(LED_PIN, GPIO.HIGH)  # Zet de LED aan
            step_motor(50)  # Draai de stepper motor
        else:  # Als de switch niet is ingedrukt
            GPIO.write(LED_PIN, GPIO.LOW)  # Zet de LED uit
            reset_motor()  # Reset de stepper motor

        # Wacht even voordat de volgende meting
        time.sleep(1)

except KeyboardInterrupt:
    # Opruimen bij het afsluiten van het script
    GPIO.cleanup()
    client.disconnect()
    print("Script gestopt.")