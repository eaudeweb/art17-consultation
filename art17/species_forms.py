# encoding: utf-8

from wtforms import Form, Field, DecimalField, FormField
from wtforms.validators import Required


class Trend(Form):

    trend = Field()
    period_min = Field()
    period_max = Field()


class Range(Form):

    surface_area = DecimalField(
            u"Suprafață (km²)",
            [Required(u"Suprafața este obligatorie")])
    method = Field(u"Metoda utilizată - suprafața arealului")
    trend_short = FormField(Trend, separator='.')


class SpeciesComment(Form):

    range = FormField(Range, separator='.')

    def populate_obj(self, obj):
        obj.range_surface_area = self.range.data['surface_area']
        obj.range_method = self.range.data['method']
        obj.range_trend = self.range.trend_short.data['trend']
        obj.range_trend_period = '%s-%s' % (
            self.range.trend_short.data['period_min'],
            self.range.trend_short.data['period_max'])
