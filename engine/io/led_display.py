import time
from smbus import SMBus

# for i2c expander
bus = SMBus(1) # Port 1 used on REV2

if __name__ == '__main__':
    while True:
        bus.write_byte(0x24, 0xff)
        time.sleep(1)
        bus.write_byte(0x24, 0x00)
        time.sleep(1)
