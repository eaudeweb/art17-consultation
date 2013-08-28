class GenericRecord(object):

    def __init__(self, row):
        self.row = row

    def _split_period(self, year_string):
        if year_string:
            return "(%s-%s)" % (year_string[:4], year_string[4:])
        else:
            return ""

    def _get_trend(self, name, qualifier=''):
        period = getattr(self.row, '%s_trend%s_period' % (name, qualifier))
        trend = getattr(self.row, '%s_trend%s' % (name, qualifier))
        return "%s %s" % (trend, self._split_period(period))

    def _get_conclusion(self, name):
        assessment_col = 'conclusion_%s' % name
        trend_col = 'conclusion_%s_trend' % name
        if name == 'future':
            trend_col += 's'
        assessment = getattr(self.row, assessment_col)
        trend = getattr(self.row, trend_col)
        if trend:
            return "%s (%s)" % (assessment, trend)
        else:
            return assessment

    def _get_reference_value(self, name):
        if name == 'range':
            ideal = self.row.range_surface_area
        elif name == 'population':
            ideal = (self.row.population_minimum_size or
                     self.row.population_alt_minimum_size)
        else:
            raise RuntimeError("Unknown name %r" % name)

        favourable = getattr(self.row, 'complementary_favourable_%s' % name)
        favourable_op = getattr(self.row, 'complementary_favourable_%s_op' % name)
        favourable_x = getattr(self.row, 'complementary_favourable_%s_x' % name)
        method = getattr(self.row, 'complementary_favourable_%s_method' % name)

        if favourable:
          rv = favourable

        elif favourable_op:
          rv = "%s %s" % (favourable_op, ideal)

        elif favourable_x:
          rv = "Unknown"

        else:
          rv = "N/A"

        if method:
            return "%s (method: %s)" % (rv, method)

        else:
            return rv
