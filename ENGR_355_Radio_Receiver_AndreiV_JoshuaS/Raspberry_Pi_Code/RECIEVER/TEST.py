from machine import SoftI2C, Pin
import time

i2c = SoftI2C(scl=Pin(2), sda=Pin(3), freq=100000)
time.sleep(0.05)  # 50ms delay for device boot

print("Reading register 0x02 on MS5351M (0x60 address)")
try:
    data = bytearray(1)
    i2c.readfrom_mem_into(0x60, 0x02, data)
    print("Register 0x02:", data[0])
except Exception as e:
    print("Error:", e)
