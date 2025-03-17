import wiringpi
import time
from smbus2 import SMBus, i2c_msg

# I2C-bus instellingen voor Orange Pi
bus = SMBus(0)  # Orange Pi gebruikt I2C-bus 2
bh1750_address = 0x23  # BH1750 standaard I2C-adres

LED_1 = 3
LED_2 = 4

wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_1, 1)
wiringpi.pinMode(LED_2, 1)

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

while True:
    light_level = get_value(bus, bh1750_address)
    
    if(light_level > 300):
        print(f"Light: {light_level:.1f} lux")
        wiringpi.digitalWrite(LED_2, 0)
        wiringpi.digitalWrite(LED_1, 1)
        time.sleep(1)
    else:
        print(f"Light: {light_level:.1f} lux")
        wiringpi.digitalWrite(LED_1, 0)
        wiringpi.digitalWrite(LED_2, 1)
        time.sleep(1)


