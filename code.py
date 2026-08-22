import time
import struct
import board
import digitalio
import usb_hid
from adafruit_seesaw.seesaw import Seesaw

# Find the gamepad device that boot.py created
gamepad = None
for device in usb_hid.devices:
    if device.usage_page == 0x01 and device.usage == 0x05:
        gamepad = device
        break

# JoyWing buttons: seesaw pin -> gamepad button bit
joy_buttons = {6: 0, 7: 1, 10: 2, 9: 3, 14: 4}   # A, B, X, Y, SELECT
mask = 0
for p in joy_buttons:
    mask |= (1 << p)

i2c = board.I2C()
ss = Seesaw(i2c)
ss.pin_mode_bulk(mask, ss.INPUT_PULLUP)

# Buttons wired straight to the Feather's GPIO: pin -> gamepad button bit
gpio_map = {
    board.IO10: 5,   # START
    board.IO3:  6,   # Bumper 1
    board.IO5:  7,   # Bumper 2
    board.IO12: 8,   # Hotkey
}
gpio_buttons = {}
for pin, bit in gpio_map.items():
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    gpio_buttons[io] = bit

def range_map(v, in_min, in_max, out_min, out_max):
    return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# --- Startup delay ---
# The Feather boots faster than a Pi Zero. Waiting here lets the Pi finish
# booting enough to register the controller, so it connects on its own.
# Tune this number: ~25 s works for a Pi Zero reaching EmulationStation in ~60 s.
time.sleep(25)

while True:
    buttons = 0
    held = ss.digital_read_bulk(mask)
    for pin, bit in joy_buttons.items():
        if not held & (1 << pin):
            buttons |= (1 << bit)
    for io, bit in gpio_buttons.items():
        if not io.value:
            buttons |= (1 << bit)

    # Stick. If left/right or up/down read wrong, see the tuning notes below.
    x = max(-127, min(127, range_map(ss.analog_read(3), 0, 1023, -127, 127)))
    y = max(-127, min(127, range_map(ss.analog_read(2), 0, 1023, -127, 127)))

    if gamepad:
        gamepad.send_report(struct.pack("<Hbb", buttons, x, y))

    time.sleep(0.02)
