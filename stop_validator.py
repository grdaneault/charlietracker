import json

import time

from opc import Client

with open("stop_configuration.json") as config:
    stops = json.load(config)



current_led = 0
total_leds = 64 * 8
client = Client('localhost:7890')

while True:
    for stop_id, stop_config in stops.items():
        print("%s: %s (%s)" % (stop_config['led'], stop_id, stop_config['name']))
        pixels = [(0, 0, 0)] * total_leds
        pixels[stop_config['led']] = (255, 255, 255)
        client.put_pixels(pixels)
        client.put_pixels(pixels)
        time.sleep(0.1)
