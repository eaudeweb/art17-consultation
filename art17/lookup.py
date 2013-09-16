# encoding: utf-8

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

LU_FV_RANGE_OP_FUNCT_OPTIONS =[
    (u'≈', u"≈ approximately equal to"),
    (u'>', u"> more than"),
    (u'≫', u"≫ much more than"),
    (u'<', u"< less than"),
]

LU_FV_RANGE_OP_FUNCT = dict(LU_FV_RANGE_OP_FUNCT_OPTIONS)


LU_FV_RANGE_OP_OPTIONS =[
    (u'≈', u"≈ approximately equal to"),
    (u'>', u"> more than"),
    (u'≫', u"≫ much more than"),
]

LU_FV_RANGE_OP = dict(LU_FV_RANGE_OP_OPTIONS)


METHODS_USED_OPTIONS = [
    ('3', u"Complete survey/Complete survey or a statistically robust estimate"),
    ('2', u"Estimate based on partial data with some extrapolation and/or modelling"),
    ('1', u"Estimate based on expert opinion with no or minimal sampling"),
    ('0', u"Absent data"),
]

METHODS_USED = dict(METHODS_USED_OPTIONS)


TREND_OPTIONS = [
    ('+', u"+ (În creștere)"),
    ('-', u"- (În scădere)"),
    ('0', u"0 (Stabil)"),
    ('x', u"x (Necunoscut)"),
]

TREND_NAME = dict(TREND_OPTIONS)


CONCLUSION_OPTIONS = [
    ('FV', u"Favourable"),
    ('U1', u"Inadequate"),
    ('U2', u"Bad"),
    ('XX', u"Unknown"),
]

CONCLUSIONS = dict(CONCLUSION_OPTIONS)
