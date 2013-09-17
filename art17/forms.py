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
            validators=[Required(u"Suprafața este obligatorie")])
    method = SelectField(choices=METHODS_USED_OPTIONS,
            validators=[Required(u"Metoda utilizată este obligatorie")])
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    conclusion = FormField(Conclusion)

    def __init__(self, *args, **kwargs):
        super(Range, self).__init__(*args, **kwargs)
        self.reference_value.op.choices=EMPTY_CHOICE + LU_FV_RANGE_OP_OPTIONS


class Population(Form):
    size = FormField(PopulationSize)
    method = SelectField(choices=METHODS_USED_OPTIONS,
            validators=[Required(u"Metoda utilizată este obligatorie")])
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    conclusion = FormField(Conclusion)

    def __init__(self, *args, **kwargs):
        super(Population, self).__init__(*args, **kwargs)
        self.reference_value.op.choices=EMPTY_CHOICE + LU_FV_RANGE_OP_FUNCT_OPTIONS


class Habitat(Form):
    surface_area = DecimalField(
            validators=[Required(u"Suprafața este obligatorie")])
    date = TextField(
            validators=[Required(u"Anul sau perioada sunt obligatorii")])
    method = SelectField(choices=METHODS_USED_OPTIONS,
            validators=[Required(u"Metoda utilizată este obligatorie")])
    quality = SelectField(choices=QUALITY_OPTIONS,
            validators=[Required(u"Valoarea calitǎții este obligatorie")])
    quality_explanation = TextAreaField(
            validators=[Required(u"Metoda este obligatorie")])
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    area_suitable = DecimalField(
            validators=[Required(u"Suprafața este obligatorie")])
    conclusion = FormField(Conclusion)

class SpeciesComment(Form):

    range = FormField(Range)
    population = FormField(Population)
    habitat = FormField(Habitat)

    def populate_obj(self, obj):
        schemas.flatten_species_commentform(self.data, obj)


class HabitatComment(Form):

    range = FormField(Range)

    def populate_obj(self, obj):
        schemas.flatten_habitat_commentform(self.data, obj)
