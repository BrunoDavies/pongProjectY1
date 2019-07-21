import smbus
import time
import RPi.GPIO as GPIO #IO library

import constants as cfg



I2CADDR_1 = 0x21
I2CADDR_2 = 0x24
# CMD_CODE = int("0b1000 0000", 2)
CMD_CODE = 0x80
MAX_1 = 252
MIN_1 = 192

MAX_2 = 1000
MIN_2 = 192

last_value_1 = 0
last_value_2 = 0

bus = smbus.SMBus(1)

def reverse_mask(n):
    n = (n & 0x00FF)<<8 | (n & 0xFF00)>>8
    return n

def rem_four_lyfe(x):
    return(x & 0x0fff)


def get_value_1(sample_size=cfg.ADC_SAMPLE_SIZE):
    global MAX_1, MIN_1, last_value_1
    total = 0
    if not cfg.USE_ADAPTING_AVERAGE:
        for _ in range(sample_size):
            try:
                bus.write_byte(I2CADDR_1, CMD_CODE)
                tmp = bus.read_word_data(I2CADDR_1, 0x00)
                total += reverse_mask(rem_four_lyfe(tmp))
            except OSError:
                pass
        val = int(total / sample_size)
    else:
        bus.write_byte(I2CADDR_1, CMD_CODE)
        tmp = bus.read_word_data(I2CADDR_1, 0x00)
        val = reverse_mask(rem_four_lyfe(tmp))
    val = val >> 6
    val = (val - MIN_1) / (MAX_1 - MIN_1)
    if cfg.USE_ADAPTING_AVERAGE:
        last_value_1 = (last_value_1 * ADAPTING_AVERAGE_DECAY + val) / (
            1 + cfg.ADAPTING_AVERAGE_DECAY)
        return last_value_1
    else:
        return val

def get_value_2(sample_size=cfg.ADC_SAMPLE_SIZE):
    global MAX_2, MIN_2
    total = 0
    for _ in range(sample_size):
        try:
            GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print(GPIO.input(11))
        except OSError:
            pass
    # val = int(total / sample_size) >> 6
    # return (val - MIN_2) / (MAX_2 - MIN_2)



GPIO.setwarnings(False) #disable runtime warnings
GPIO.setmode(GPIO.BCM) #use Broadcom GPIO names
# GPIO.setup(cfg.PI_CONTROLLER_GPIO_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def button_1_check():
    return GPIO.input(9) != 1

def button_2_check():
    return GPIO.input(10) != 1
