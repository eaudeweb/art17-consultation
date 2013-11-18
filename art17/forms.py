# encoding: utf-8

import json
from wtforms import (Form as Form_base, FormField as FormField_base,
                     TextField, TextAreaField, DecimalField, SelectField,
                     IntegerField, SelectMultipleField, BooleanField)
from wtforms.validators import Required, Optional, NumberRange
from wtforms.widgets import HTMLString, html_params
from werkzeug.datastructures import MultiDict

from art17 import models
from art17.lookup import (
    TREND_OPTIONS,
    CONCLUSION_OPTIONS,
    METHODS_USED_OPTIONS,
    LU_FV_RANGE_OP_OPTIONS,
    LU_FV_RANGE_OP_FUNCT_OPTIONS,
    LU_POP_NUMBER_OPTIONS,
    LU_POP_NUMBER_RESTRICTED_OPTIONS,
    LU_REASONS_FOR_CHANGE_OPTIONS,
    QUALITY_OPTIONS,
    METHODS_PRESSURES_OPTIONS,
    METHODS_THREATS_OPTIONS
)
from art17 import schemas

EMPTY_CHOICE = [('', "")]


def all_fields(form):
    for field in form:
        if hasattr(field, 'form'):
            for subfield in all_fields(field.form):
               yield subfield
        else:
            yield field


class MultipleHiddenWidget(object):

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []
        for val in field.data:
            html.append(self.render_input(field, val))
        return HTMLString(''.join(html))

    @classmethod
    def render_input(cls, field, val):
        val = json.dumps(val)
        return HTMLString('<input type="hidden" %s %s />' % (
                                                html_params(name=field.name),
                                                html_params(value=val)))


class MultipleJSONField(SelectMultipleField):

    widget = MultipleHiddenWidget()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('coerce', json.loads)
        super(MultipleJSONField, self).__init__(*args, **kwargs)

    def iter_choices(self):
        return []

    def pre_validate(self, form):
        if self.data:
            check_list = []
            for obj in self.data:
                if obj in check_list:
                    raise ValueError('Duplicate values')
                check_list.append(obj)

    def render_input(self, val):
        return self.widget.render_input(self, val)


class MeasureField(BooleanField):

    def _value(self):
        return '1'

    
class FormValidator(object):

    def __init__(self, form):
        self.validation_form = form

    def __call__(self, form, field):
        data = field.data

        form = self.validation_form()
        for i,d in enumerate(data):
            form.process(MultiDict(d))
            if not form.validate():
                raise ValueError('Invalid values on line ' + str(i + 1))


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


class PressureForm(Form):

    pressure = SelectField(default='')
    ranking = SelectField(default='')
    pollutions = SelectMultipleField(default='')

    def __init__(self, *args, **kwargs):
        super(PressureForm, self).__init__(*args, **kwargs)
        self.pressure.choices = EMPTY_CHOICE + [(p[0], '%s. %s' % p) for p in models.db.session.query(
                                            models.LuThreats.code,
                                            models.LuThreats.name)]
        self.ranking.choices = EMPTY_CHOICE + list(models.db.session.query(
                                            models.LuRanking.code,
                                            models.LuRanking.name))
        self.pollutions.choices = [(p[0], '%s %s' % p) for p in models.db.session.query(
                                            models.LuPollution.code,
                                            models.LuPollution.name)]


class Pressures(Form):

    pressures_method = SelectField(default='', choices=EMPTY_CHOICE + METHODS_PRESSURES_OPTIONS)
    pressures = MultipleJSONField(default='', validators=[FormValidator(PressureForm)])


class MeasuresForm(Form):

    measurecode = SelectField(default='')
    type_legal = MeasureField(default=False)
    type_administrative = MeasureField(default=False)
    type_contractual = MeasureField(default=False)
    type_recurrent = MeasureField(default=False)
    type_oneoff = MeasureField(default=False)
    rankingcode = SelectField(default='')
    location_inside = MeasureField(default=False)
    location_outside = MeasureField(default=False)
    location_both = MeasureField(default=False)
    broad_evaluation_maintain = MeasureField(default=False)
    broad_evaluation_enhance = MeasureField(default=False)
    broad_evaluation_longterm = MeasureField(default=False)
    broad_evaluation_noeffect = MeasureField(default=False)
    broad_evaluation_unknown = MeasureField(default=False)
    broad_evaluation_notevaluat_18 = MeasureField(default=False)

    def __init__(self, *args, **kwargs):
        super(MeasuresForm, self).__init__(*args, **kwargs)
        self.measurecode.choices = EMPTY_CHOICE + list(models.db.session.query(
                                                       models.LuMeasures.code,
                                                       models.LuMeasures.name))
        self.rankingcode.choices = EMPTY_CHOICE + list(models.db.session.query(
                                                       models.LuRanking.code,
                                                       models.LuRanking.name))


class Measures(Form):

    measures = MultipleJSONField(default='')


class SpeciesComment(Form):

    range = FormField(Range)
    population = FormField(Population)
    habitat = FormField(Habitat)
    pressures = FormField(Pressures)
    measures = FormField(Measures)
    future_prospects = FormField(Conclusion)
    overall_assessment = FormField(Conclusion)
    report_observation = TextAreaField(validators=[Optional()])
    generalstatus = SelectField(default='1')

    def __init__(self, *args, **kwargs):
        super(SpeciesComment, self).__init__(*args, **kwargs)
        self.generalstatus.choices = models.db.session.query(
                                            models.LuPresence.code,
                                            models.LuPresence.name)

    def custom_validate(self):
        generalstatus_field = self.generalstatus
        fields = list(f for f in all_fields(self) if f != generalstatus_field)
        empty = [f for f in fields if not f.data]

        if empty and len(empty) == len(fields):
            if generalstatus_field.data == '1':
                fields[0].errors.append(u"Completați cel puțin o valoare.")
                return False

        return True


class HabitatComment(Form):

    range = FormField(Range)
    coverage = FormField(Coverage)
    structure = FormField(Conclusion)
    future_prospects = FormField(Conclusion)
    overall_assessment = FormField(Conclusion)
    report_observation = TextAreaField(validators=[Optional()])

    def custom_validate(self):
        fields = list(all_fields(self))
        empty = [f for f in fields if not f.data]

        if empty and len(empty) == len(fields):
            fields[0].errors.append(u"Completați cel puțin o valoare.")
            return False

        return True
