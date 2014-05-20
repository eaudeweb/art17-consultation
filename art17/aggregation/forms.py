from wtforms import SelectField, Form
from wtforms.widgets import Select, html_params, HTMLString
from art17.aggregation.utils import get_datasets


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
