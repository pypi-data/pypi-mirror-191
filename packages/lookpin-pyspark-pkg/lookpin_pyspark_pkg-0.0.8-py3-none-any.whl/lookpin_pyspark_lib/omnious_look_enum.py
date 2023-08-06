import enum

class OmniousLookEnum(enum.Enum):
    ethnic = 1
    casual = 2
    marine = 3
    military = 4
    outdoor = 5
    party = 6
    preppy = 7
    punk = 8
    resort = 9
    feminine = 10
    wedding = 11
    country = 12
    officelook = 13
    hippie = 14
    retro = 15



def get_omnious_look_enum(key):
    if key is None:
        return 0
    else:
        return OmniousLookEnum[key.replace('/', '').replace('-', '')].value
