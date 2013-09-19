# encoding: utf-8

from wtforms import (Form, FormField as FormField_base,
                     TextField, TextAreaField, DecimalField, SelectField)
from wtforms.validators import Required, Optional
from art17.lookup import (TREND_OPTIONS,
                          CONCLUSION_OPTIONS,
                          METHODS_USED_OPTIONS,
                          LU_FV_RANGE_OP_OPTIONS,
                          LU_FV_RANGE_OP_FUNCT_OPTIONS,
                          LU_POP_NUMBER_OPTIONS,
                          LU_POP_NUMBER_RESTRICTED_OPTIONS,
                          QUALITY_OPTIONS)
from art17 import schemas

EMPTY_CHOICE = [('', "")]


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

    op = SelectField(validators=[Optional()])
    number = DecimalField(validators=[Optional()])
    method = TextAreaField()


class Conclusion(Form):

    value = SelectField(choices=EMPTY_CHOICE + CONCLUSION_OPTIONS,
                        validators=[Optional()])
    trend = SelectField(choices=EMPTY_CHOICE + TREND_OPTIONS,
                        validators=[Optional()])


class PopulationValue(Form):
    unit = SelectField(validators=[Optional()])
    min = DecimalField(
            validators=[Optional(u"Mǎrimea trebuie sǎ fie de tip numeric")])
    max = DecimalField(
            validators=[Optional(u"Mǎrimea trebuie sǎ fie de tip numeric")])


class PopulationSize(Form):
    population = FormField(PopulationValue)
    population_alt = FormField(PopulationValue)

    def __init__(self, *args, **kwargs):
        super(PopulationSize, self).__init__(*args, **kwargs)
        self.population.unit.choices = EMPTY_CHOICE + LU_POP_NUMBER_RESTRICTED_OPTIONS
        self.population_alt.unit.choices = EMPTY_CHOICE + LU_POP_NUMBER_OPTIONS


class Range(Form):

    surface_area = DecimalField(
            validators=[Optional(u"Mǎrimea trebuie sǎ fie de tip numeric")])
    method = SelectField(choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    conclusion = FormField(Conclusion)

    def __init__(self, *args, **kwargs):
        super(Range, self).__init__(*args, **kwargs)
        self.reference_value.op.choices=EMPTY_CHOICE + LU_FV_RANGE_OP_OPTIONS


class Population(Form):
    size = FormField(PopulationSize)
    method = SelectField(choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    conclusion = FormField(Conclusion)

    def __init__(self, *args, **kwargs):
        super(Population, self).__init__(*args, **kwargs)
        self.reference_value.op.choices=EMPTY_CHOICE + LU_FV_RANGE_OP_FUNCT_OPTIONS


class Habitat(Form):
    surface_area = DecimalField(
            validators=[Optional(u"Mǎrimea trebuie sǎ fie de tip numeric")])
    date = TextField(validators=[Optional()])
    method = SelectField(choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
    quality = SelectField(choices=EMPTY_CHOICE + QUALITY_OPTIONS)
    quality_explanation = TextAreaField()
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    area_suitable = DecimalField(
            validators=[Optional(u"Mǎrimea trebuie sǎ fie de tip numeric")])
    conclusion = FormField(Conclusion)


class Coverage(Form):
    surface_area = DecimalField(
            validators=[Optional(u"Mǎrimea trebuie sǎ fie de tip numeric")])
    date = TextField(validators=[Optional()])
    method = SelectField(choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    conclusion = FormField(Conclusion)

    def __init__(self, *args, **kwargs):
        super(Coverage, self).__init__(*args, **kwargs)
        self.reference_value.op.choices=EMPTY_CHOICE + LU_FV_RANGE_OP_FUNCT_OPTIONS

class SpeciesComment(Form):

    range = FormField(Range)
    population = FormField(Population)
    habitat = FormField(Habitat)
    future_prospects = FormField(Conclusion)
    overall_assessment = FormField(Conclusion)


class HabitatComment(Form):

    range = FormField(Range)
    coverage = FormField(Coverage)
    structure = FormField(Conclusion)
    future_prospects = FormField(Conclusion)
    overall_assessment = FormField(Conclusion)
