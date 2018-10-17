# MusicBox Interface Protype
# Metro M0 - Circuit Python 3.x

# //// IMPORTS
import board
import time
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import touchio
import rotaryio




# //// BOARD SETUP
# One pixel connected internally!
dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

leftbutton = DigitalInOut(board.D2)
leftbutton.direction = Direction.INPUT
leftbutton.pull = Pull.UP

middlebutton = DigitalInOut(board.D3)
middlebutton.direction = Direction.INPUT
middlebutton.pull = Pull.UP

# External rotary encoder
leftencoder = rotaryio.IncrementalEncoder(board.D5, board.D6)
middleencoder = rotaryio.IncrementalEncoder(board.D7, board.D8)




# //// PURE FUNCTIONS
def buttonIsDown(button):  # returns intuitive button press value
	#
    return not button.value

def anythingHasChanged():
	if prev_left_button_down != buttonIsDown(leftbutton):
		return True
	elif prev_left_encoder_position != leftencoder.position:
		return True
	elif prev_middle_button_down != buttonIsDown(middlebutton):
		return True
	elif prev_middle_encoder_position != middleencoder.position:
		return True
	return False

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


# //// COMMANDS
def doPrintToSerial():
	print(
	"LeftEncoder: %d" % leftencoder.position,
	"/",
	"LeftButton: %d" % buttonIsDown(leftbutton),
	"/",
	"MiddleEncoder: %d" % middleencoder.position,
	"/",
	"MiddleButton: %d" % buttonIsDown(middlebutton)
	)
	pass


# //// HELPERS / UPDATES
def updateEveryControl():
	global prev_left_button_down
	global prev_left_encoder_position
	global prev_middle_button_down
	global prev_middle_encoder_position

	prev_left_button_down = buttonIsDown(leftbutton)
	prev_left_encoder_position = leftencoder.position
	prev_middle_button_down = buttonIsDown(middlebutton)
	prev_middle_encoder_position = middleencoder.position




# //// VARIABLES ////
i = 0

prev_left_button_down = buttonIsDown(leftbutton)
prev_left_encoder_position = leftencoder.position
prev_middle_button_down = buttonIsDown(middlebutton)
prev_middle_encoder_position = middleencoder.position




# //// MAIN LOOP ////
while True:
	# INITIAL SETUP


	# COMMANDS
	if anythingHasChanged():
		updateEveryControl()
		doPrintToSerial()


	# CONTINUOUS
	# spin internal LED around! autoshow is on
	dot[0] = wheel(i & 255)
	# set onboard LED to match either Button
	led.value = buttonIsDown(leftbutton) or buttonIsDown(middlebutton)

	i = (i+1) % 256  # run from 0 to 255
	time.sleep(0.01) # make bigger to slow down