class GenericRecord(object):

    def __init__(self, row):
        self.row = row

    def _split_period(self, year_string):
        if year_string:
            return "(%s-%s)" % (year_string[:4], year_string[4:])
        else:
            return ""

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
