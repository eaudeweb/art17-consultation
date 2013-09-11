# encoding: utf-8

from wtforms import (Form, FormField as FormField_base,
                     TextField, TextAreaField, DecimalField, SelectField)
from wtforms.validators import Required, Optional
from art17.common import TREND_OPTIONS, CONCLUSION_OPTIONS
from art17 import schemas

EMPTY_CHOICE = [('', "--")]


class FormField(FormField_base):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('separator', '.')
        super(FormField, self).__init__(*args, **kwargs)


class Period(Form):

    start = TextField()
    end = TextField()


class Trend(Form):

    trend = SelectField(choices=EMPTY_CHOICE + TREND_OPTIONS,
                        validators=[Optional()])
    period = FormField(Period)


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
        schemas.flatten_species(self.data, obj)


class HabitatComment(Form):

    range = FormField(Range)

    def populate_obj(self, obj):
        schemas.flatten_habitat(self.data, obj)
