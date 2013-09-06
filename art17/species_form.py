# encoding: utf-8

from wtforms import Form, DecimalField
from wtforms.validators import Required


class SpeciesCommentForm(Form):

    range_surface_area = DecimalField(u"Suprafață (km²)",
            [Required(u"Suprafața este obligatorie")])
