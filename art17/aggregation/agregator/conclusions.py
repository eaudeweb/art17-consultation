FV = 'FV'
U1 = 'U1'
U2 = 'U2'
XX = 'XX'


def get_habitat_conclusion_future(code, region):
    return FV


def get_species_conclusion_future(code, region):
    return FV


def get_overall_conclusion(concs):
    if concs.count(XX) > 2:
        return XX
    if FV in concs and not (U1 in concs or U2 in concs):
        return FV
    if U1 in concs and U2 not in concs:
        return U1
    if U2 in concs:
        return U2
    return ''


def get_overall_habitat_conclusion(result):
    concs = [
        result.conclusion_range or '', result.conclusion_area or '',
        result.conclusion_structure or '', result.conclusion_future or ''
    ]
    return get_overall_conclusion(concs)


def get_overall_species_conclusion(result):
    concs = [
        result.conclusion_range or '', result.conclusion_population or '',
        result.conclusion_habitat or '', result.conclusion_future or '',
    ]
    return get_overall_conclusion(concs)
