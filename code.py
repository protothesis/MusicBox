# Metro IO demo
# Welcome to CircuitPython 2.2.0 :)


# //// IMPORTS
import board
import time
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import touchio
# import simpleio
import rotaryio




# //// BOARD SETUP
# One pixel connected internally!
dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup
buttons = []
for p in [board.D2, board.D3]:
    button = DigitalInOut(p)
    button.direction = Direction.INPUT
    button.pull = Pull.UP
    buttons.append(button)

# External rotary encoder
encoder = rotaryio.IncrementalEncoder(board.D5, board.D6)
# TODO
	# add support for second rotary encoder
	# perhaps some sort of schema like buttons[] above




# //// PURE FUNCTIONS
def buttonIsDown(num):  # returns intuitive button press value
	#
    return not buttons[num].value




# //// COMMANDS
def doPrintToSerial():
	print(
	"LeftEncoder: %d" % encoder.position,
	"/",
	"LeftButton: %d" % buttonIsDown(0),
	"/",
	"MiddleEncoder: %d" % 0,  # encoder.position,
	"/",
	"MiddleButton: %d" % buttonIsDown(1)
	)
	pass




# //// HELPERS / UPDATES
def wheel(pos):  # Helper to give us a nice color swirl
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]

def encoderHasChanged():  # updates the encoder position value (and value for serial message)
	global last_encoded_position
	global serial_message_encoder

	global encoder_has_changed
	current_encoded_position = encoder.position

	if last_encoded_position is None or current_encoded_position != last_encoded_position:
		encoder_has_changed = True
		serial_message_encoder = current_encoded_position
		# doPrintToSerial()
	else:
		encoder_has_changed = False

	last_encoded_position = current_encoded_position 

    


# //// VARIABLES ////
i = 0

last_encoded_position = None
encoder_has_changed = None
serial_message_encoder = None




# //// MAIN LOOP ////
while True:
	# INITIAL SETUP


	# COMMANDS
	if encoder_has_changed:
		# doPrintToSerial()
		pass


	# CONTINUOUS
	encoderHasChanged()

  	# spin internal LED around! autoshow is on
	dot[0] = wheel(i & 255)
	# set onboard LED to match either Button
	led.value = buttonIsDown(0) or buttonIsDown(1)


	if buttonIsDown(0):
		# print("Left Button 'D2' Pressed!!!", end ="\t")
		pass

	if buttonIsDown(1):
		# print("Middle Button 'D3' Pressed!", end ="\t")
		pass


	# update the serial message (for easy feedback)
	doPrintToSerial()

	i = (i+1) % 256  # run from 0 to 255
	time.sleep(0.01) # make bigger to slow down