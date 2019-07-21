#####
#
# PyGlow
#
#####
#
# Python module to control Pimoronis PiGlow
# [http://shop.pimoroni.com/products/piglow]
#
# * test.py - set brightness for each color individually
#
#####
import time
import math

from .py_glow import PyGlow
pyglow = PyGlow()


def play_animation():
    arm = 1
    for i in range(63):
        pyglow.arm(arm, 0)
        arm = (arm + 1) % 3 + 1
        pyglow.arm(arm, int(100 + 100 * math.sin(time.time() * 3)))
        time.sleep(0.06)
    pyglow.all(0)

if __name__ == '__main__':
    play_animation()
