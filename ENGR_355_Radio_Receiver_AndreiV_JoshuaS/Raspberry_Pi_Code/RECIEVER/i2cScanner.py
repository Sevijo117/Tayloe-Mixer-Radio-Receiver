# ropython i2c scanner
# Scanner i2c en MicroPython | MicroPython i2c scanner
# Renvoi l'adresse en decimal et hexa de chaque device connecte sur le bus i2c
# Return decimal and hexa adress of each i2c device
# https://projetsdiy.fr - https://diyprojects.io (dec. 2017)
# I2C Scanner for twisted pins
from machine import Pin, SoftI2C
import time

# Twisted GPIO pins (adjusted for hardware mistake!)
scl_pin = Pin(2, Pin.OUT, Pin.PULL_UP)
sda_pin = Pin(3, Pin.OUT, Pin.PULL_UP)

# SoftI2C to avoid hardware mapping limitations
i2c = SoftI2C(scl=scl_pin, sda=sda_pin, freq=100000)  # 100 kHz typical I2C speed

print("I2C SCANNER - Twisted Pins")

while True:
    devices = i2c.scan()
    if len(devices) == 0:
        print("No I2C devices found!")
    else:
        print("I2C devices found:", len(devices))
        for device in devices:
            print(" - Address:", hex(device))
    time.sleep(2)  # Scan every 2 seconds