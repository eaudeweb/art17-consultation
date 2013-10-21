# encoding: utf-8

from wtforms import (Form as Form_base, FormField as FormField_base,
                     TextField, TextAreaField, DecimalField, SelectField,
                     IntegerField)
from wtforms.validators import Required, Optional, NumberRange
from art17.lookup import (TREND_OPTIONS,
                          CONCLUSION_OPTIONS,
                          METHODS_USED_OPTIONS,
                          LU_FV_RANGE_OP_OPTIONS,
                          LU_FV_RANGE_OP_FUNCT_OPTIONS,
                          LU_POP_NUMBER_OPTIONS,
                          LU_POP_NUMBER_RESTRICTED_OPTIONS,
                          LU_REASONS_FOR_CHANGE_OPTIONS,
                          QUALITY_OPTIONS)
from art17 import schemas

EMPTY_CHOICE = [('', "")]


def all_fields(form):
    for field in form:
        if hasattr(field, 'form'):
            for subfield in all_fields(field.form):
               yield subfield
        else:
            yield field


class FormField(FormField_base):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('separator', '.')
        super(FormField, self).__init__(*args, **kwargs)


class Form(Form_base):

    def validate(self):
        if not super(Form, self).validate():
            return False

        return self.custom_validate()

    def custom_validate(self):
        return True


class Period(Form):

    start = IntegerField(label=u"an de început",
                         validators=[Optional(), NumberRange(1900, 2100)])
    end = IntegerField(label=u"an de sfârșit",
                       validators=[Optional(), NumberRange(1900, 2100)])


def set_required_error_message(field):
    message = u'Completați câmpul "%s"' % field.label.text
    field.errors.append(message)


class Trend(Form):

    trend = SelectField(choices=EMPTY_CHOICE + TREND_OPTIONS,
                        default='',
                        label=u"tendință",
                        validators=[Optional()])
    period = FormField(Period)

    def custom_validate(self):
        fields = [self.period.start, self.period.end, self.trend]
        empty = [f for f in fields if not f.data]

        if empty and len(empty) < len(fields):
            for field in empty:
                set_required_error_message(field)
            return False

        return True


class ReferenceValue(Form):

    op = SelectField(default='', label=u"operator", validators=[Optional()])
    number = DecimalField(label=u"suprafață", validators=[Optional()])
    method = TextAreaField()

    def custom_validate(self):
        fields = [self.op, self.number]
        empty = [f for f in fields if not f.data]

        if empty and len(empty) < len(fields):
            for field in empty:
                set_required_error_message(field)
            return False

        return True


class Conclusion(Form):

    value = SelectField(choices=EMPTY_CHOICE + CONCLUSION_OPTIONS,
                        default='',
                        validators=[Optional()])
    trend = SelectField(choices=EMPTY_CHOICE + TREND_OPTIONS,
                        default='',
                        validators=[Optional()])


class PopulationValue(Form):
    unit = SelectField(default='', validators=[Optional()])
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
    method = SelectField(default='',
                         choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    conclusion = FormField(Conclusion)

    def __init__(self, *args, **kwargs):
        super(Range, self).__init__(*args, **kwargs)
        self.reference_value.op.choices=EMPTY_CHOICE + LU_FV_RANGE_OP_OPTIONS


class Population(Form):
    size = FormField(PopulationSize)
    method = SelectField(default='',
                         choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
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
    method = SelectField(default='',
                         choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
    quality = SelectField(default='',
                          choices=EMPTY_CHOICE + QUALITY_OPTIONS)
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
    method = SelectField(default='',
                         choices=EMPTY_CHOICE + METHODS_USED_OPTIONS)
    trend_short = FormField(Trend)
    trend_long = FormField(Trend)
    reference_value = FormField(ReferenceValue)
    conclusion = FormField(Conclusion)

    def __init__(self, *args, **kwargs):
        super(Coverage, self).__init__(*args, **kwargs)
        self.reference_value.op.choices=EMPTY_CHOICE + LU_FV_RANGE_OP_FUNCT_OPTIONS

class SpeciesConclusion(Form):

    range = FormField(Range)
    population = FormField(Population)
    habitat = FormField(Habitat)
    future_prospects = FormField(Conclusion)
    overall_assessment = FormField(Conclusion)

    def custom_validate(self):
        fields = list(all_fields(self))
        empty = [f for f in fields if not f.data]

        if empty and len(empty) == len(fields):
            fields[0].errors.append(u"Completați cel puțin o valoare.")
            return False

        return True


class HabitatConclusion(Form):

    range = FormField(Range)
    coverage = FormField(Coverage)
    structure = FormField(Conclusion)
    future_prospects = FormField(Conclusion)
    overall_assessment = FormField(Conclusion)

    def custom_validate(self):
        fields = list(all_fields(self))
        empty = [f for f in fields if not f.data]

        if empty and len(empty) == len(fields):
            fields[0].errors.append(u"Completați cel puțin o valoare.")
            return False

        return True
