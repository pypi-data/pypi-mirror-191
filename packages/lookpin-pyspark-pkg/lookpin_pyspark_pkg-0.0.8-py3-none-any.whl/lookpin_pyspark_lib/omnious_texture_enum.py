import enum

class OmniousTextureEnum(enum.Enum):
    mouton = 1
    rubber = 2
    bandage = 3
    vinylpvc = 4
    corduroy = 5
    linen = 6
    felt = 7
    mesh = 8
    leather = 9
    crochet = 10
    silksatin = 11
    denim = 12
    knit = 13
    plasticpvc = 14
    lace = 15
    woolcashmere = 16
    tweed = 17
    syntheticpolyester = 18
    fishnet = 19
    fur = 20
    patent = 21
    angora = 22
    suede = 23
    raffia = 24
    nylon = 25
    fleece = 26
    padding = 27
    jersey = 28
    velvet = 29
    spandex = 30
    metal = 31
    neoprene = 32
    sequinglitter = 33
    canvas = 34
    cotton = 35
    gold = 36
    satinsilk = 37
    chiffon = 38
    jacquard = 39
    crystal = 40
    silk = 41



def get_omnious_texture_enum(key):
    if key is None:
        return 0
    else:
        return OmniousTextureEnum[key.replace('/', '').replace('-', '')].value