# encoding: utf-8

from wtforms import (Form, FormField as FormField_base,
                     TextField, TextAreaField, DecimalField, SelectField)
from wtforms.validators import Required, Optional
from art17.common import TREND_OPTIONS, CONCLUSION_OPTIONS

EMPTY_CHOICE = [('', "--")]


class FormField(FormField_base):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('separator', '.')
        super(FormField, self).__init__(*args, **kwargs)


class Trend(Form):

    trend = SelectField(choices=EMPTY_CHOICE + TREND_OPTIONS,
                        validators=[Optional()])
    period_min = TextField()
    period_max = TextField()


class ReferenceValue(Form):

    op = TextField()
    number = DecimalField(validators=[Optional()])


class Conclusion(Form):

    value = SelectField(choices=EMPTY_CHOICE + CONCLUSION_OPTIONS,
                        validators=[Optional()])
    trend = TextField()


class Range(Form):

    surface_area = DecimalField(
            validators=[Required(u"Suprafața este obligatorie")])
    method = TextField()
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    reference_method = TextAreaField()
    conclusion = FormField(Conclusion)


class SpeciesComment(Form):

    range = FormField(Range)

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
