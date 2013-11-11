# encoding: utf-8


LU_REASONS_FOR_CHANGE_OPTIONS = [
    ('a', u"genuine change"),
    ('b', u"improved knowledge/more accurate data"),
    ('c', u"use of different method (e.g. `Range tool`)"),
]

LU_REASONS_FOR_CHANGE = dict(LU_REASONS_FOR_CHANGE_OPTIONS)

LU_POP_NUMBER_OPTIONS = [
    ('i', u"number of individuals"),
    ('adults', u"number of adults"),
    ('subadults', u"number of subadults"),
    ('bfemales', u"number of breeding females"),
    ('cmales', u"number of calling males"),
    ('males', u"number of males"),
    ('p', u"number of pairs"),
    ('shoots', u"number of shoots"),
    ('tufts', u"number of tufts"),
    ('fstems', u"number of flowering stems"),
    ('localities', u"number of localities"),
    ('colonies', u"number of colonies"),
    ('logs', u"number of inhabited logs"),
    ('trees', u"number of inhabited trees"),
    ('stones', u"number of inhabited stones/boulders"),
    ('area', u"area coverd by population in m2"),
    ('length', u"length of inhabited feature in km"),
    ('grids1x1', u"number of map 1x1 km grid cells"),
    ('grids5x5', u"number of map 5x5 km grid cells"),
    ('grids10x10', u"number of map 10x10 km grid cells"),
]

LU_POP_NUMBER = dict(LU_POP_NUMBER_OPTIONS)

LU_POP_NUMBER_RESTRICTED_OPTIONS = [
    ('i', u"number of individuals"),
    ('colonies', u"number of colonies"),
    ('logs', u"number of inhabited logs"),
    ('trees', u"number of inhabited trees"),
    ('stones', u"number of inhabited stones/boulders"),
    ('area', u"area coverd by population in m2"),
    ('length', u"length of inhabited feature in km"),
]

LU_POP_NUMBER_RESTRICTED = dict(LU_POP_NUMBER_RESTRICTED_OPTIONS)

LU_FV_RANGE_OP_FUNCT_OPTIONS =[
    (u'≈', u"aproximativ egal cu"),
    (u'>', u"mai mare decǎt"),
    (u'≫', u"mult mai mare decǎt"),
    (u'<', u"mai micǎ decǎt"),
]

LU_FV_RANGE_OP_FUNCT = dict(LU_FV_RANGE_OP_FUNCT_OPTIONS)


LU_FV_RANGE_OP_OPTIONS =[
    (u'≈', u"aproximativ egal cu"),
    (u'>', u"mai mare decǎt"),
    (u'≫', u"mult mai mare decǎt"),
]

LU_FV_RANGE_OP = dict(LU_FV_RANGE_OP_OPTIONS)


METHODS_USED_OPTIONS = [
    ('3', u"Inventarieri complete sau o estimare statistică solidă"),
    ('2', u"Estimări prin extrapolări și/sau modelări bazate pe date parțiale"),
    ('1', u"Estimǎri bazate numai pe opinia expertului, fără sau cu eșantionare minimală"),
    ('0', u"Date lipsǎ"),
]

METHODS_USED = dict(METHODS_USED_OPTIONS)


TREND_OPTIONS = [
    ('+', u"În creștere"),
    ('-', u"În descreștere"),
    ('0', u"Stabilă"),
    ('x', u"Necunoscută"),
]

TREND_NAME = dict(TREND_OPTIONS)


CONCLUSION_OPTIONS = [
    ('FV', u"Favorabilǎ"),
    ('U1', u"Nefavorabil-Inadecvat"),
    ('U2', u"Nefavorabil-Rau"),
    ('XX', u"Necunoscutǎ"),
]

CONCLUSIONS = dict(CONCLUSION_OPTIONS)


QUALITY_OPTIONS = [
    ('1', u"Bunǎ"),
    ('2', u"Moderatǎ"),
    ('3', u"Neadecvatǎ"),
    ('4', u"Necunoscutǎ"),
]

QUALITY = dict(QUALITY_OPTIONS)


METHODS_PRESSURES_OPTIONS = [
    ('3', u"Bazat numai pe opinia expertului"),
    ('2', u"Bazat în principal pe opinia expertului sau alte date"),
    ('1', u"Bazat exclusiv sau în principal pe date reale provenite din teren")
]

METHODS_PRESSURES = dict(METHODS_PRESSURES_OPTIONS)


METHODS_THREATS_OPTIONS = [
    ('2', u"Modelări"),
    ('1', u"Opinia expertului"),
]

METHODS_THREATS = dict(METHODS_THREATS_OPTIONS)


GENERALSTATUS_CHOICES = [
    ('ok', u"specia este prezentă"),
    ('x-taxonomic', u"rezervă taxonomică"),
    ('x-scientific', u"rezervă științifică"),
    ('x-extinct', u"specia a dispărut"),
]
