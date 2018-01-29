#https://learn.pimoroni.com/tutorial/tanya/santabot-xmas-timer
import datetime
import time

#currentYear = datetime.now().year
while True:
    xmas = datetime.datetime(2018, 12, 25) - datetime.datetime.now()
    #xmas = datetime.datetime(currentYear, 12, 25) - datetime.datetime.now()
    daysleft = xmas.days
    hoursleft = xmas.seconds/3600

    print("Ho ho ho! It's %i days and %i hours until xmas!" %(daysleft, hoursleft))
