import json

import time
from mbta import Vehicle
from collections import defaultdict

from led import Colors
from opc import Client

stop_configuration = json.load(open("stop_configuration.json"))

INBOUND_INDICATOR = 53
OUTBOUND_INDICATOR = 54


def get_vehicle_positions():
    vehicles = Vehicle.get_list(params={"filter[route]": "741,742,749,751,Blue,Green-B,Green-C,Green-D,Green-E,Mattapan,Orange,Red", "include": "stop,route"})

    vehicles_by_stop = defaultdict(list)
    for vehicle in vehicles:
        stop = vehicle.stop
        if stop is not None:
            if stop.parent_station is not None:
                stop = stop.parent_station
            vehicles_by_stop[stop.id].append(vehicle)
    return vehicles_by_stop


def light_stop(leds, stop, vehicle):
    if stop not in stop_configuration:
        raise ValueError("Unexpected stop!")

    led_id = stop_configuration[stop]['led']

    color_name = "SILVER"
    if "Red" in vehicle.route.name or "Mattapan" in vehicle.route.name:
        color_name = "RED"
    elif "Green" in vehicle.route.name:
        color_name = "GREEN"
    elif "Blue" in vehicle.route.name:
        color_name = "BLUE"
    elif "Orange" in vehicle.route.name:
        color_name = "ORANGE"

    if vehicle.status == 'STOPPED_AT':
        leds[led_id] = getattr(Colors, color_name)
    elif vehicle.status == 'INCOMING_AT':
        # print("should blink " + vehicle.stop.name)
        leds[led_id] = getattr(Colors, color_name + "_BLINK")
    # elif vehicle.status == 'IN_TRANSIT_TO':
    #     leds[led_id] = getattr(Colors, color_name + "_BLINK_DARK")


def update(client, positions, direction, duration=30):
    leds = [Colors.BLACK] * 512
    if direction == "Inbound":
        leds[INBOUND_INDICATOR] = Colors.RED
    else:
        leds[OUTBOUND_INDICATOR] = Colors.RED
    for stop_id, vehicles in positions.items():
        # if len(vehicles) > 1:
            # print(stop_configuration[stop_id]['name'] + ": " + (", ".join(vehicle.status + " " + vehicle.direction_name for vehicle in vehicles)))

        for vehicle in vehicles:
            if vehicle.direction_name == direction:
                light_stop(leds, stop_id, vehicle)
            elif direction in vehicle.stop.name:
                light_stop(leds, stop_id, vehicle)
            else:
                if stop_id == "place-pktrm":
                    if vehicle.direction_name == "Eastbound" and direction == "Inbound":
                        light_stop(leds, stop_id, vehicle)
                    elif vehicle.direction_name == "Westbound" and direction == "Outbound":
                        light_stop(leds, stop_id, vehicle)
                    elif vehicle.direction_name == "Southbound" and direction == "Inbound":
                        light_stop(leds, stop_id, vehicle)
                    elif vehicle.direction_name == "Northbound" and direction == "Outbound":
                        light_stop(leds, stop_id, vehicle)
                elif stop_id == "place-dwnxg":
                    if vehicle.direction_name == "Northbound" and direction == "Outbound":
                        light_stop(leds, stop_id, vehicle)
                    elif vehicle.direction_name == "Southbound" and direction == "Inbound":
                        light_stop(leds, stop_id, vehicle)
        # light_stop(leds, stop_id, None)

    client.put_pixels([px.render(0) for px in leds])
    for i in range(duration):
        client.put_pixels([px.render(i) for px in leds])
        time.sleep(1)
        i += 1

def main():
    client = Client('localhost:7890')

    while True:
        print('Updating... ', end="")
        positions = get_vehicle_positions()
        print("done")
        print("inbound... ")
        update(client, positions, "Inbound", 10)
        print("outbound... ")
        update(client, positions, "Outbound", 10)

if __name__ == '__main__':
    main()


