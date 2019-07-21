import RPi.GPIO as GPIO
from smbus import SMBus


#for i2c expander
LED_CODES = {
    0: 0x01,
    1: 0x02,
    2: 0x04,
    3: 0x08,
    4: 0x10,
    5: 0x20,
    6: 0x40,
    7: 0x80
}

# for onboard LEDs
LED_PINS = {
    0: 5,
    1: 6,
    2: 12,
    3: 13,
    4: 16,
    5: 19,
    6: 20,
    7: 26
}

# for i2c expander
bus = SMBus(1) # Port 1 used on REV2

# for onboard LEDs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for gpio_pin in LED_PINS.values():
    GPIO.setup(gpio_pin, GPIO.OUT)

last_led = 0

for i in range(8):
    GPIO.output(LED_PINS[i], GPIO.LOW)

def led_on(led):
    global last_led
    # replace 0x38 with whatever addr the i2c expander has
    bus.write_byte(0x38, ~LED_CODES[led])
    if last_led != led:
        GPIO.output(LED_PINS[led], GPIO.HIGH)
        GPIO.output(LED_PINS[last_led], GPIO.LOW)
        last_led = led


if __name__ == "__main__":
    import time
    for i in range(8):
        GPIO.output(LED_PINS[i], GPIO.LOW)
    while True:
        GPIO.output(12, GPIO.HIGH)
        time.sleep(1)

    i = 0
    while True:
        led_on(i)
        i = (i + 1) % 8
        time.sleep(0.25)
