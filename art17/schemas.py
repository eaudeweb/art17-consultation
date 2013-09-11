def flatten_species(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']
    obj.range_trend = struct['range']['trend_short']['trend']
    obj.range_trend_period = '%s-%s' % (
        struct['range']['trend_short']['period_min'],
        struct['range']['trend_short']['period_max'])
    obj.range_trend_long = struct['range']['trend_long']['trend']
    obj.range_trend_long_period = '%s-%s' % (
        struct['range']['trend_long']['period_min'],
        struct['range']['trend_long']['period_max'])
    obj.complementary_favourable_range_op = \
        struct['range']['reference_value']['op']
    obj.complementary_favourable_range = \
        struct['range']['reference_value']['number']
    obj.complementary_favourable_range_method = \
        struct['range']['reference_method']
    obj.conclusion_range = struct['range']['conclusion']['value']
    obj.conclusion_range_trend = struct['range']['conclusion']['trend']



def flatten_habitat(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']
    obj.range_trend = struct['range']['trend_short']['trend']
    obj.range_trend_period = '%s-%s' % (
        struct['range']['trend_short']['period_min'],
        struct['range']['trend_short']['period_max'])
    obj.range_trend_long = struct['range']['trend_long']['trend']
    obj.range_trend_long_period = '%s-%s' % (
        struct['range']['trend_long']['period_min'],
        struct['range']['trend_long']['period_max'])
    obj.complementary_favourable_range_op = \
        struct['range']['reference_value']['op']
    obj.complementary_favourable_range = \
        struct['range']['reference_value']['number']
    obj.complementary_favourable_range_method = \
        struct['range']['reference_method']
    obj.conclusion_range = struct['range']['conclusion']['value']
    obj.conclusion_range_trend = struct['range']['conclusion']['trend']
