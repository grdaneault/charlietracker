import time

from opc import Client

current_led = 0
total_leds = 64 * 8
client = Client('localhost:7890')

strands = [(2, 49), (257, 308), (450, 497)]


# while True:
#     for start, end in

while True:
    pixels = [(0, 0, 0)] * total_leds
    pixels[current_led] = (0, 255, 0)
    client.put_pixels(pixels)
    client.put_pixels(pixels)  # duplicate command so that it happens instantly
    print("Currently Lit: %3d.  Next? [%3d]" % (current_led, current_led + 1), end="")
    current_led = int(input() or current_led + 1)
    # current_led += 1
    current_led %= total_leds
    # time.sleep(0.1)

