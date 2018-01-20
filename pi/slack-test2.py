import json
import requests
import sys
import os
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

cmd = '/opt/vc/bin/vcgencmd measure_temp'
line = os.popen(cmd).readline().strip()
temp = line.split('=')[1].split("'")[0]
#status= 'I\'m awake and my current CPU temperature is '+temp+' C'
msg_emoji = getEmoji(int(float(temp)))

#print(temp)
#print(msg_emoji)
status= 'I\'m awake and my current CPU temperature is '+temp+' C '+msg_emoji

print(status)

