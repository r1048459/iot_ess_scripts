import time
from smbus2 import SMBus, i2c_msg
from bmp280 import BMP280
import paho.mqtt.client as mqtt

bus = SMBus(0)  
bmp280_address = 0x77  
bh1750_address = 0x23

bmp280 = BMP280(i2c_addr=bmp280_address, i2c_dev=bus)

bus.write_byte(bh1750_address, 0x10)
bytes_read = bytearray(2)

interval = 15

def get_value(bus, bh1750_address):
    write = i2c_msg.write(bh1750_address, [0x10])
    read = i2c_msg.read(bh1750_address, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0]&3) << 8) + bytes_read[1])/1.2

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "orangepi/sensors"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)  

while True:
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    light_level = get_value(bus, bh1750_address)
    
    print(f"Temperature: {temperature:.1f}°C, Pressure: {pressure:.1f} hPa, Light: {light_level:.1f} lux")

    MQTT_DATA = f"field1={temperature}&field2={pressure}&field3={light_level}&status=MQTTPUBLISH"
    print(f"Sending: {MQTT_DATA}")

    try:
        result = client.publish(topic=MQTT_TOPIC, payload=MQTT_DATA, qos=0, retain=False)
        print(f"MQTT Publish Result: {result.rc}")
        client.reconnect()

        time.sleep(interval)

    except Exception as e:
        print(f"MQTT Error: {e}")
        client.reconnect() 
        time.sleep(5)
