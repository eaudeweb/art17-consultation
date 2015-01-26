""" load data from previous aggregations, used in trend calculation

    Example response:
    {
        '2110-ALP':
        [
            {
                'year': 2012,
                'range_surface_area': 200
                ...
            },
            {
                'year': 2006,
                'range_surface_area': 210
            }
        ],
        '2110-STE':
        [
           ...
        ]
        ...
    }
"""


def get_subject_prev(subject, dataset):
    if subject == 'species':
        return load_species_prev(dataset)
    elif subject == 'habitat':
        return load_habitat_prev(dataset)
    raise NotImplementedError


def load_species_prev(dataset):
    return {}


def load_habitat_prev(dataset):
    return {}
