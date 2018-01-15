# import GPIO
import RPi.GPIO as GPIO
import time #import time module

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT)

#flash the LED on pin 29 when booted up
for x in range(1, 10):
        GPIO.output(29,False)
        time.sleep(.5)
        GPIO.output(29,True)
        time.sleep(1)
          
finally:
    GPIO.cleanup()
