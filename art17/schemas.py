def flatten_trend(trend_struct, obj, prefix):
    setattr(obj, prefix, trend_struct['trend'])
    setattr(obj, prefix + '_period', '%s-%s' % (trend_struct['period_min'],
                                                trend_struct['period_max']))


def flatten_species(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')

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

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')

    obj.complementary_favourable_range_op = \
        struct['range']['reference_value']['op']
    obj.complementary_favourable_range = \
        struct['range']['reference_value']['number']
    obj.complementary_favourable_range_method = \
        struct['range']['reference_method']
    obj.conclusion_range = struct['range']['conclusion']['value']
    obj.conclusion_range_trend = struct['range']['conclusion']['trend']
