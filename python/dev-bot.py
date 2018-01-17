# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import os #added so we can shut down OK
import time #import time module

# Set variables for the GPIO motor pins
# Check pins
indicatorLight = 25
pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7

# Set the GPIO Pin modes
# Leave as BCM instead of BOARD for now
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(indicatorLight, GPIO.OUT)
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)

for x in range(1, 10):
	GPIO.output(indicatorLight,False)
	time.sleep(.5)
	GPIO.output(indicatorLight,True)
	time.sleep(1)

# Define Drive Functions - might need tweaking
# Turn all motors off
def StopMotors():
	GPIO.output(pinMotorAForwards, 0)
	GPIO.output(pinMotorABackwards, 0)
	GPIO.output(pinMotorBForwards, 0)
	GPIO.output(pinMotorBBackwards, 0)

# Turn both motors forwards
def Forwards():
	GPIO.output(pinMotorAForwards, 1)
	GPIO.output(pinMotorABackwards, 0)
	GPIO.output(pinMotorBForwards, 1)
	GPIO.output(pinMotorBBackwards, 0)

# Turn both motors backwards
def Backwards():
	GPIO.output(pinMotorAForwards, 0)
	GPIO.output(pinMotorABackwards, 1)
	GPIO.output(pinMotorBForwards, 0)
	GPIO.output(pinMotorBBackwards, 1)

# Turn left 
def Left(): 
	GPIO.output(pinMotorAForwards, 0)
	GPIO.output(pinMotorABackwards, 1)
	GPIO.output(pinMotorBForwards, 1)
	GPIO.output(pinMotorBBackwards, 0)
	
# Turn Right 
def Right(): 
	GPIO.output(pinMotorAForwards, 1)
	GPIO.output(pinMotorABackwards, 0)
	GPIO.output(pinMotorBForwards, 0)
	GPIO.output(pinMotorBBackwards, 1)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
	while True:
		char = screen.getch()
		if char == ord('q'):
			break
		if char == ord('S'): # Added for shutdown on capital S
			os.system ('sudo shutdown now') # shutdown right now!
		elif char == curses.KEY_UP:
			Forwards()
		elif char == curses.KEY_DOWN:
			Backwards()
		elif char == curses.KEY_RIGHT:
			Right()
		elif char == curses.KEY_LEFT:
			Left()
		elif char == 10:
			StopMotors()

finally:
	#Close down curses properly, inc turn echo back on!
	curses.nocbreak(); screen.keypad(0); curses.echo()
	curses.endwin()
	GPIO.cleanup()
