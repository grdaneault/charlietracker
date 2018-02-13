import json
from mbta import Stop

relevant_stops = Stop.get_list(params={"filter[route]": "741,742,749,751,Blue,Green-B,Green-C,Green-D,Green-E,Mattapan,Orange,Red", "include": "stop,route"})
stop_leds = {stop.id: {"name": stop.name, "led": -1} for stop in relevant_stops}

with open("stop_configuration.json", "w") as outfile:
    json.dump(stop_leds, outfile, indent=4)
