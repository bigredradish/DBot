#!/usr/bin/env python

import sys
import time

from envirophat import light, weather
import blinkt

blinkt.set_clear_on_exit()

unit = 'hPa' # Pressure unit, can be either hPa (hectopascals) or Pa (pascals)

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()

write("--- Enviro pHAT Monitoring ---")

try:
    while True:
        rgb = light.rgb()

        output = """
		Temp: {t}c
		Pressure: {p}{unit}
		Light: {c}
		RGB: {r}, {g}, {b}
		""".format(
				unit = unit,
				t = round(weather.temperature(),2),
				p = round(weather.pressure(unit=unit),2),
				c = light.light(),
				r = rgb[0],
				g = rgb[1],
				b = rgb[2]
			)
        output = output.replace("\n","\n\033[K")
        write(output)
        lines = len(output.split("\n"))
        write("\033[{}A".format(lines - 1))
		
	blinkt.set_all(rgb[0], rgb[1], rgb[2])
	blinkt.show()
	
        time.sleep(1)
        
except KeyboardInterrupt:
    pass
