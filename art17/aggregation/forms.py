# encoding: utf-8
from wtforms import SelectField, Form, FileField, validators
from wtforms.widgets import Select, html_params, HTMLString
from art17 import models
from art17.aggregation.utils import get_habitat_checklist, \
    get_species_checklist
from art17.common import get_datasets


class OptgroupSelect(Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = 'multiple'
        html = [u'<select %s>' % html_params(name=field.name, **kwargs)]
        for value, label, selected in field.iter_choices():
            if hasattr(label, '__iter__'):
                html.append(u'<optgroup %s>' % html_params(label=value))
                for v, l, s in label:
                    html.append(self.render_option(v, l, s))
                html.append(u'</optgroup>')
            else:
                html.append(self.render_option(value, label, selected))
        html.append(u'</select>')
        return HTMLString(u''.join(html))


class OptgroupSelectField(SelectField):
    def iter_choices(self, choices=None):
        choices = choices if choices is not None else self.choices
        for value, label in choices:
            if isinstance(label, (list, tuple)):
                yield (value, self.iter_choices(label), None)
            else:
                yield (value, label, self.coerce(value) == self.data)

    def pre_validate(self, form):
        for k, v in self.choices:
            if isinstance(v, (list, tuple)):
                for k2, v2 in v:
                    if self.data == self.coerce(k2):
                        return
            elif self.data == self.coerce(k):
                return
        else:
            raise ValueError(self.gettext(u'Not a valid choice'))


class PreviewForm(Form):
    subject = OptgroupSelectField(default='', widget=OptgroupSelect())

    def __init__(self, page=None, checklist_id=None, **kwargs):
        super(PreviewForm, self).__init__(**kwargs)

        if page == 'habitat':
            qs = list(
                get_habitat_checklist(dataset_id=checklist_id, distinct=True))
            qs_dict = dict(qs)
            qs.sort(key=lambda x: x[0])
        elif page == 'species':
            orig_qs = list(
                get_species_checklist(dataset_id=checklist_id, distinct=True))
            qs_dict = dict(orig_qs)

            orig_qs = {a[0]: a for a in orig_qs}
            qs = []
            for group in models.LuGrupSpecie.query.all():
                species = (
                    models.LuHdSpecies.query
                    .filter_by(group_code=group.code)
                    .order_by(models.LuHdSpecies.speciesname)
                )
                species = [
                    orig_qs[str(s.code)]
                    for s in species if str(s.code) in orig_qs
                ]
                qs.append((group.description, species))
        else:
            raise NotImplementedError()
        self.subject.choices = qs
        self.qs_dict = qs_dict


class CompareForm(Form):
    dataset1 = SelectField()
    dataset2 = SelectField()

    def __init__(self, *args, **kwargs):
        super(CompareForm, self).__init__(*args, **kwargs)
        datasets = [(str(d.id), d) for d in get_datasets()]
        self.dataset1.choices = datasets
        self.dataset2.choices = datasets

    def validate(self):
        res = super(CompareForm, self).validate()
        if self.dataset1.data == self.dataset2.data:
            self.dataset1.errors.append('Cannot compare to self')
            return False
        return res


class WhatForm(Form):
    CHOICES = ((0, 'Toate'), (1, 'Valide'), (2, 'Nevalide'))
    what = SelectField(choices=CHOICES, default=0, coerce=int)


class RefValuesForm(Form):
    excel_doc = FileField(u'Document Excel')

    def validate_excel_doc(self, field):
        if not field.data or not field.data.filename.endswith('.xlsx'):
            raise validators.ValidationError(
                u'Sunt acceptate doar fișiere în format Excel')
