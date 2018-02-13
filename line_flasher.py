import json

import time
from mbta import Stop
from collections import defaultdict

from led import Colors
from opc import Client

stop_configuration = json.load(open("stop_configuration.json"))

routes = "Green-B,Green-C,Green-D,Green-E,Orange,749,751,Mattapan,Red,742,741,Blue".split(",")
stops = {}
for route in routes:
    stops[route] = Stop.get_list(params={"filter[route]": route})


def light_stop(leds, stop, route_name):
    if stop.parent_station is not None:
        stop = stop.parent_station
    stop = stop.id
    if stop not in stop_configuration:
        raise ValueError("Unexpected stop!", stop)

    led_id = stop_configuration[stop]['led']

    color_name = "SILVER"
    if "Red" in route_name or "Mattapan" in route_name:
        color_name = "RED"
    elif "Green" in route_name:
        color_name = "GREEN"
    elif "Blue" in route_name:
        color_name = "BLUE"
    elif "Orange" in route_name:
        color_name = "ORANGE"

    leds[led_id] = getattr(Colors, color_name)


def loop(client, delay=0.5):
    for route in routes:
        leds = [Colors.BLACK] * 512
        for stop in stops[route]:
            light_stop(leds, stop, route)

        client.put_pixels([px.render(0) for px in leds])
        client.put_pixels([px.render(0) for px in leds])
        time.sleep(delay)


def main():
    client = Client('localhost:7890')
    while True:
        loop(client)

if __name__ == '__main__':
    main()