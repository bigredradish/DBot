# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import os
import sys
import time
from datetime import datetime
#from twython import Twython # sudo pip install twython may need pip?
#from subprocess import call
import json
import requests

#define the emojis
def getEmoji(temp):
    if temp >= 60:
        emoji = ':crab:'
    elif temp >= 50:
        emoji = ':hamster:'
    elif temp >= 40:
        emoji = ':bear:'
    elif temp >= 30:
        emoji = ':panda_face:'
    else:
        emoji = ':monkey_face:'
    return emoji

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url = 'https://hooks.slack.com/services/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'

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

#flash indicator to know that script has loaded
for x in range(1, 5):
	GPIO.output(indicatorLight,False)
	time.sleep(.5)
	GPIO.output(indicatorLight,True)
	time.sleep(1)

#take a photo
#photo_name = 'test.jpg'
#cmd = 'raspistill -t 500 -w 1024 -h 768 -vf -hf -o /home/pi/camera/' + photo_name   
#call ([cmd], shell=True)         #shoot the photo  

#tweet status
#CONSUMER_KEY = 'XWvTXK9uLkadYuI6ELUlmyIV0'
#CONSUMER_SECRET = 'Tjv48OH0LITfehhPCgSfHPWDjbIcVX5VyCol06Ic50bkFezO1O'
#ACCESS_KEY = '5751542-LdgUu0MnWmoYXMqkrbJwtsAgHmI95kUvRu46aCSSFH'
#ACCESS_SECRET = 'kgWU0GfrLVToVLeSxkSrhgViEjxpOqT2WkWvIQg85lgvy'

#api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

cmd = '/opt/vc/bin/vcgencmd measure_temp'
line = os.popen(cmd).readline().strip()
temp = line.split('=')[1].split("'")[0]
#photo = open('/home/pi/camera/' + photo_name, 'rb')

#api.update_status_with_media(media=photo, status=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' DBot says: I\'m awake and my current CPU temperature is '+temp+' C. I can see:')
msg_emoji = getEmoji(int(float(temp)))

status= 'I\'m awake and my current CPU temperature is '+temp+' C '+msg_emoji
slack_data = {'text': status}

response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

# DO RoBoT Stuff
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
			response = requests.post(
    				webhook_url, data=json.dumps(slack_data),
    				headers={'Content-Type': 'application/json'}
			)
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
	#api.update_status(status=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' DBot says: Shutting Down...')
	slack_data = {'text': "Quitting Program..."}

	response = requests.post(
    		webhook_url, data=json.dumps(slack_data),
    		headers={'Content-Type': 'application/json'}
	)
	if response.status_code != 200:
    		raise ValueError(
        		'Request to slack returned an error %s, the response is:\n%s'
        		% (response.status_code, response.text)
 		)		
