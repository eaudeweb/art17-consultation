# encoding: utf-8

from wtforms import (Form, FormField,
                     TextField, TextAreaField, DecimalField, SelectField)
from wtforms.validators import Required, Optional
from art17.common import TREND_OPTIONS, CONCLUSION_OPTIONS

EMPTY_CHOICE = [('', "--")]


class Trend(Form):

    trend = SelectField(choices=EMPTY_CHOICE + TREND_OPTIONS,
                        validators=[Optional()])
    period_min = TextField()
    period_max = TextField()


class ReferenceValue(Form):

    op = TextField()
    number = DecimalField()


class Conclusion(Form):

    value = SelectField(choices=EMPTY_CHOICE + CONCLUSION_OPTIONS,
                        validators=[Optional()])
    trend = TextField()


class Range(Form):

    surface_area = DecimalField(
            validators=[Required(u"Suprafața este obligatorie")])
    method = TextField(u"Metoda utilizată - suprafața arealului")
    trend_short = FormField(Trend, separator='.')
    trend_long = FormField(Trend, separator='.')
    reference_value = FormField(ReferenceValue, separator='.')
    reference_method = TextAreaField()
    conclusion = FormField(Conclusion, separator='.')


class SpeciesComment(Form):

    range = FormField(Range, separator='.')

    def populate_obj(self, obj):
        obj.range_surface_area = self.range.data['surface_area']
        obj.range_method = self.range.data['method']
        obj.range_trend = self.range.trend_short.data['trend']
        obj.range_trend_period = '%s-%s' % (
            self.range.trend_short.data['period_min'],
            self.range.trend_short.data['period_max'])
        obj.range_trend_long = self.range.trend_long.data['trend']
        obj.range_trend_long_period = '%s-%s' % (
            self.range.trend_long.data['period_min'],
            self.range.trend_long.data['period_max'])
        obj.complementary_favourable_range_op = \
            self.range.reference_value.data['op']
        obj.complementary_favourable_range = \
            self.range.reference_value.data['number']
        obj.complementary_favourable_range_method = \
            self.range.reference_method.data
        obj.conclusion_range = self.range.conclusion.data['value']
        obj.conclusion_range_trend = self.range.conclusion.data['trend']
