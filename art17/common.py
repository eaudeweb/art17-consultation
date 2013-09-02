# encoding: utf-8

import flask

TREND_NAME = {
    "+": u"În creștere",
    "-": u"În scădere",
    "0": u"Stabil",
    "x": u"Necunoscut",
}

common = flask.Blueprint('common', __name__)


@common.app_context_processor
def inject_constants():
    return {'TREND_NAME': TREND_NAME}


class GenericRecord(object):

    def __init__(self, row):
        self.row = row

    def _split_period(self, year_string):
        if year_string:
            # u2011: non-breaking hyphen
            return u"(%s\u2011%s)" % (year_string[:4], year_string[4:])
        else:
            return ""

    def _get_trend(self, name, qualifier=''):
        period = getattr(self.row, '%s_trend%s_period' % (name, qualifier))
        trend = getattr(self.row, '%s_trend%s' % (name, qualifier))
        return {
            'trend': trend,
            'period': self._split_period(period),
        }

    def _get_magnitude(self, name, qualifier=''):
        mag_min = getattr(self.row, '%s_trend%s_magnitude_min' % (name, qualifier))
        mag_max = getattr(self.row, '%s_trend%s_magnitude_max' % (name, qualifier))
        return {
            'min': mag_min,
            'max': mag_max,
        }

    def _get_conclusion(self, name):
        return getattr(self.row, 'conclusion_%s' % name)

    def _get_reference_value(self, name, ideal):
        favourable = getattr(self.row, 'complementary_favourable_%s' % name)
        favourable_op = getattr(self.row, 'complementary_favourable_%s_op' % name)
        favourable_x = getattr(self.row, 'complementary_favourable_%s_x' % name)
        method = getattr(self.row, 'complementary_favourable_%s_method' % name)

        if favourable:
            value = favourable

        elif favourable_op:
            value = "%s%s" % (favourable_op, ideal)

        elif favourable_x:
            value = "Unknown"

        else:
            value = "N/A"

        return {
            'value': value,
            'method': method,
        }
