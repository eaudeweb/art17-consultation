# encoding: utf-8


LU_REASONS_FOR_CHANGE_OPTIONS = [
    ('a', u"Schimbare reală"),
    ('b', u"Cunoștințe îmbunătățite / date mai precise"),
    ('c', u"Utilizarea unor metode diferite (ex. `Range tool`)"),
]

LU_REASONS_FOR_CHANGE = dict(LU_REASONS_FOR_CHANGE_OPTIONS)


LU_FV_RANGE_OP_FUNCT_OPTIONS =[
    (u'≈', u"Aproximativ egal cu"),
    (u'>', u"Mai mare decǎt"),
    (u'≫', u"Mult mai mare decǎt"),
    (u'<', u"Mai micǎ decǎt"),
]

LU_FV_RANGE_OP_FUNCT = dict(LU_FV_RANGE_OP_FUNCT_OPTIONS)


LU_FV_RANGE_OP_OPTIONS =[
    (u'≈', u"Aproximativ egal cu"),
    (u'>', u"Mai mare decǎt"),
    (u'≫', u"Mult mai mare decǎt"),
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
    ('=', u"Stabilă"),
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
    ('Good', u"Bunǎ"),
    ('Moderate', u"Moderatǎ"),
    ('Bad', u"Neadecvatǎ"),
    ('Unknown', u"Necunoscutǎ"),
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
