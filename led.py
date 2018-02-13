class Color:
    def __init__(self, r, g, b, blink=False):
        self.r = r
        self.g = g
        self.b = b
        self.blink = blink
        self.color = (r, g, b)

    def render(self, frame):
        if not self.blink or frame % 2 == 0:
            return self.color
        return (0, 0, 0)


class Colors:
    RED = Color(255, 0, 0)
    RED_BLINK = Color(255, 0, 0, True)
    RED_BLINK_DARK = Color(64, 0, 0, True)
    ORANGE = Color(255, 165, 0)
    ORANGE_BLINK = Color(255, 165, 0, True)
    ORANGE_BLINK_DARK = Color(64, 32, 0, True)
    GREEN = Color(0, 255, 0)
    GREEN_BLINK = Color(0, 255, 0, True)
    GREEN_BLINK_DARK = Color(0, 64, 0, True)
    BLUE = Color(0, 0, 255)
    BLUE_BLINK = Color(0, 0, 255, True)
    BLUE_BLINK_DARK = Color(0, 0, 64, True)
    SILVER = Color(255, 255, 255)
    SILVER_BLINK = Color(255, 255, 255, True)
    SILVER_BLINK_DARK = Color(64, 64, 64, True)
    BLACK = Color(0, 0, 0)
