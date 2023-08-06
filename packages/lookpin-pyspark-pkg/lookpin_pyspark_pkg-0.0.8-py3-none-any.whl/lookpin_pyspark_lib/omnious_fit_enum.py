import enum

class OmniousFitEnum(enum.Enum):
    tight = 1
    normal = 2
    loose = 3
    oversized = 4
    skinny = 5
    loosebeggy = 6
    wide = 7


def get_omnious_fit_enum(key):
    if key is None:
        return 0
    else:
        return OmniousFitEnum[key.replace('/', '').replace('-', '')].value
