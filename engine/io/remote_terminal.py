import constants as cfg

def get_output():
    from serial import Serial
    from serial.serialutil import SerialException

    # make connection to terminal
    try:
        serial_port = Serial("/dev/ttyAMA0", 9600)
    except SerialException:
        print("failed to create serial connection")

    # create handle
    def to_remote(x):
        x = str(x).encode()
        serial_port.write(x)

    return to_remote
import constants as cfg

def get_output():
    from serial import Serial
    from serial.serialutil import SerialException

    # make connection to terminal
    try:
        serial_port = Serial("/dev/ttyAMA0", 9600)
    except SerialException:
        print("failed to create serial connection")

    # create handle
    def to_remote(x):
        x = str(x).encode()
        serial_port.write(x)

    return to_remote
