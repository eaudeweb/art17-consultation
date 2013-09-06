# encoding: utf-8

from wtforms import Form, DecimalField, FormField
from wtforms.validators import Required


class Range(Form):

    surface_area = DecimalField(
            u"Suprafață (km²)",
            [Required(u"Suprafața este obligatorie")])


class SpeciesComment(Form):

    range = FormField(Range)
