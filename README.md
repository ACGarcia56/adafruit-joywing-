adafruit-joywing
FeatherS2 + Joy FeatherWing — Retro Handheld Controller

Everything you need to turn an Unexpected Maker FeatherS2 + Adafruit Joy FeatherWing into a USB gamepad for RetroPie (or any PC). Save this for when the new JoyWing arrives.

What you need
Unexpected Maker FeatherS2 (ESP32-S2 board with native USB-C)
Adafruit Joy FeatherWing (stacks on top — joystick + A/B/X/Y/Select)
CircuitPython 10.x installed on the FeatherS2
The adafruit_seesaw library folder in /lib
(Optional) Extra push-buttons for Start, two bumpers, and a hotkey
What's included
boot.py — the full gamepad descriptor (16 buttons + stick). Goes in the root of CIRCUITPY.
code.py — the complete version with JoyWing A/B/X/Y/Select, a Start button (IO10), two bumpers (IO3/IO5), and a hotkey (IO12), including the 25-second startup delay that fixes the sync timing.
Where each file goes and how to save them (the Notepad++ "All files" trick, so they don't become .txt).
The library step (adafruit_seesaw into /lib).
The critical reset rule — boot.py only takes effect on a full power-cycle; code.py updates on save.
The button bit map and wiring table for the extra buttons.
Tuning notes for the quirks I ran into (swapped stick axes, inverted directions).

A couple of quick reminders for setting up a new board:

The time.sleep(25) in code.py is there for the slow Pi boot — if you're testing on a PC, delete that line so it responds instantly.
boot.py first, then code.py, then a full unplug/replug — that order matters.


STEP 1 — Install CircuitPython (if the new board doesn't have it)
Plug the FeatherS2 into your PC via USB-C.
Enter the UF2 bootloader: press RESET, wait ~1 second, then press BOOT (or double-tap RESET). A drive named UFTHRS2BOOT will appear.
Download the CircuitPython .UF2 for the FeatherS2 from circuitpython.org/board/unexpectedmaker_feathers2/
Drag the .UF2 onto the UFTHRS2BOOT drive. It will flash and reboot. (If you see a "copy didn't finish / F: unavailable" error mid-copy, ignore it — it's a known, harmless quirk. The CIRCUITPY drive will reappear.)


STEP 2 — Install the seesaw library
Download the CircuitPython 10.x library bundle from circuitpython.org/libraries
Copy the adafruit_seesaw FOLDER into the /lib folder on the CIRCUITPY drive. (Keep it as a folder — don't dump loose files in.)


STEP 3 — Create boot.py
Create a file named exactly boot.py in the ROOT of the CIRCUITPY drive (the same folder as code.py). This declares the board as a USB gamepad.

Editing tip (Notepad++): File → New → paste → Save As → the CIRCUITPY drive → name it boot.py → set "Save as type" to All files (*.*) so it isn't saved as boot.py.txt. Confirm it shows up as boot.py, not boot.py.txt.


STEP 4 — Create code.py
Replace everything in code.py (root of CIRCUITPY) with the version below. This is the full build: JoyWing buttons + stick, a Start button, two bumpers, and a hotkey.



STEP 5 — Activate it
Save code.py.
Full reset — unplug and replug the FeatherS2 (or press RESET). This is what makes boot.py run and turns the board into a gamepad. (Skip the reset and no gamepad will appear.)


STEP 6 — Test on a PC first (before the Pi)
Press Win + R, type joy.cpl, and press Enter.
A controller should be listed. Open its Properties.
Press buttons → they light up. Move the stick → the crosshair moves.

If that works, the gamepad is good at the USB level. Then plug it into the Pi and configure it in RetroPie (EmulationStation → Configure Input).

Tuning notes (fixes for common quirks)
Stick axes swapped (e.g. right moves the cursor down): swap the 2 and 3 in the two stick lines so the correct channel feeds each axis. This only touches code.py, so just save — no full reset needed.
A direction is inverted (e.g. left/right is backwards but on the right axis): flip that line's output range from -127, 127 to 127, -127.
Button labels don't match the silkscreen: doesn't matter here — you remap them in RetroPie's Configure Input anyway.
Editing code.py vs. boot.py: code.py changes take effect on save; boot.py changes take effect only on a full power-cycle.
