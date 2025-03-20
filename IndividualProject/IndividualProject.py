import wiringpi
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
MQTT_CLIENT_ID = "EAEWESgCDS8kPTAYFjkLERk"
MQTT_USERNAME = "EAEWESgCDS8kPTAYFjkLERk"
MQTT_PASSWORD = "0c/35VFsF8CJUw3nqMlaSCPv"
MQTT_TOPIC = "channels/2884475/publish"

# Initialisatie van WiringPi
wiringpi.wiringPiSetup()          # Gebruik WiringPi pin nummering
for pin in STEPPER_PINS:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)
wiringpi.pinMode(LED_PIN, wiringpi.OUTPUT)
wiringpi.pinMode(SWITCH_PIN, wiringpi.INPUT)

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
        for i in range(len(STEP_SEQUENCE)):
            step = STEP_SEQUENCE[i if direction == 1 else len(STEP_SEQUENCE) - 1 - i]
            for j in range(len(STEPPER_PINS)):
                wiringpi.digitalWrite(STEPPER_PINS[j], step[j])
            time.sleep(0.01)

# Functie om de stepper motor te resetten
def reset_motor():
    step_motor(50, direction=-1)  # Draai terug naar de beginpositie

# Functie om de lux-waarde te lezen van de BH1750
def read_bh1750():
    bus.write_byte(BH1750_ADDR, 0x10)  # Continu meetmodus, 1 lux resolutie
    bytes_read = bus.read_i2c_block_data(BH1750_ADDR, 0x10, 2)
    return ((bytes_read[0] << 8) + bytes_read[1]) / 1.2

# Functie om de temperatuur en druk te lezen van de BMP280
def read_bmp280():
    # BMP280 uitlezen zonder calibration_params
    data = bus.read_i2c_block_data(BMP280_ADDR, 0xFA, 6)
    temp_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp = (temp_raw / 16 - 27315) / 100  # Omrekenen naar graden Celsius

    # Druk uitlezen
    press_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    press = press_raw / 100  # Omrekenen naar hPa
    return temp, press

# Functie om data naar ThingSpeak te sturen via MQTT
def send_to_thingspeak(temp, lux, press):
    payload = f"field1={temp}&field2={lux}&field3={press}"
    try:
        client.publish(MQTT_TOPIC, payload)
        print(f"ThingSpeak Data Sent: {payload}")
    except Exception as e:
        print(f"ThingSpeak MQTT Error: {e}")

# MQTT-client initialiseren
client = mqtt.Client(client_id=MQTT_CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Hoofdprogramma
try:
    while True:
        # Lees de sensoren
        lux = read_bh1750()
        temp, press = read_bmp280()

        # Publiceer de sensorwaarden naar ThingSpeak
        send_to_thingspeak(temp, lux, press)

        # Controleer de lux-waarde en temperatuur
        if lux > 22:  # Als de lux-waarde hoger is dan 22
            step_motor(50)  # Draai de stepper motor
        elif temp < 20:  # Als de temperatuur lager is dan 20°C
            reset_motor()  # Reset de stepper motor

        # Controleer de switch
        if wiringpi.digitalRead(SWITCH_PIN) == wiringpi.LOW:  # Als de switch is ingedrukt
            wiringpi.digitalWrite(LED_PIN, wiringpi.HIGH)  # Zet de LED aan
            step_motor(50)  # Draai de stepper motor
        else:  # Als de switch niet is ingedrukt
            wiringpi.digitalWrite(LED_PIN, wiringpi.LOW)  # Zet de LED uit
            reset_motor()  # Reset de stepper motor

        # Wacht even voordat de volgende meting
        time.sleep(1)

except KeyboardInterrupt:
    # Opruimen bij het afsluiten van het script
    for pin in STEPPER_PINS:
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    wiringpi.digitalWrite(LED_PIN, wiringpi.LOW)
    client.disconnect()
    print("Script gestopt.")
