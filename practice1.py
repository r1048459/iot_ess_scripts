import time
from smbus2 import SMBus, i2c_msg
from bmp280 import BMP280
import paho.mqtt.client as mqtt

# I2C-bus instellingen voor Orange Pi
bus = SMBus(0)  # Orange Pi gebruikt I2C-bus 2
bmp280_address = 0x77  # BMP280 adres (0x76 of 0x77 afhankelijk van SDO)
bh1750_address = 0x23  # BH1750 standaard I2C-adres

# Initialiseren van sensoren
bmp280 = BMP280(i2c_addr=bmp280_address, i2c_dev=bus)

# SETUP BH1750
bus.write_byte(bh1750_address, 0x10)
bytes_read = bytearray(2)

interval = 15  # Interval in seconden

def get_value(bus, bh1750_address):
    write = i2c_msg.write(bh1750_address, [0x10])
    read = i2c_msg.read(bh1750_address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0]&3) << 8) + bytes_read[1])/1.2

# ThingSpeak MQTT-instellingen
MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "GxMIByUqDwYbMi4xOTYgNQs"
MQTT_USERNAME = "GxMIByUqDwYbMi4xOTYgNQs"
MQTT_PASSWORD = "vQvgiJsL9ee0hEdcGzXPQ/y0"
MQTT_TOPIC = "channels/2864665/publish"

# MQTT-client instellen
client = mqtt.Client(client_id=MQTT_CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    light_level = get_value(bus, bh1750_address)
    
    print(f"Temperature: {temperature:.1f}°C, Pressure: {pressure:.1f} hPa, Light: {light_level:.1f} lux")

    # JSON-formaat voor ThingSpeak
    MQTT_DATA = f"field1={temperature}&field2={pressure}&field3={light_level}&status=MQTTPUBLISH"
    print(f"Sending: {MQTT_DATA}")

    try:
        result = client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
        print(f"MQTT Publish Result: {result.rc}")  # 0 = succes
        time.sleep(interval)
    except Exception as e:
        print(f"MQTT Error: {e}")
        client.reconnect()