import enum

class OmniousColorEnum(enum.Enum):
    black = 1
    white = 2
    beige = 3
    brown = 4
    red = 5
    pink = 6
    grey = 7
    green = 8
    blue = 9
    navy = 10
    yellow = 11
    purple = 12
    orange = 13
    khaki = 14
    mint = 15
    lavender = 16
    wine = 17
    skyblue = 18
    gold = 19
    silver = 20
    rosegold = 21


def get_omnious_color_enum(key):
    if key is None:
        return 0
    else:
        return OmniousColorEnum[key.replace('/', '').replace('-', '')].value