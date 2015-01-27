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
from art17.models import (
    Dataset, DataSpeciesRegion, DataSpecies, DataHabitattypeRegion,
    DataHabitat,
)


def get_subject_prev(subject, dataset):
    if subject == 'species':
        return load_species_prev(dataset)
    elif subject == 'habitat':
        return load_habitat_prev(dataset)
    raise NotImplementedError


def load_species_prev(dataset):
    species = (
        DataSpeciesRegion.query
        .join(Dataset)
        .join(DataSpecies)
        .filter(
            Dataset.year_start <= dataset.year_start,
            Dataset.year_end <= dataset.year_end,
        )
        .with_entities(
            Dataset.year_end,
            DataSpecies.code,
            DataSpeciesRegion.region,
            DataSpeciesRegion.range_surface_area,
            DataSpeciesRegion.population_minimum_size,
            DataSpeciesRegion.population_maximum_size,
            DataSpeciesRegion.habitat_surface_area,
        )
    )
    hist_data = {}
    for s in species:
        code_region = '{}-{}'.format(s.code, s.region)
        trend_data = {
            'year': s.year_end,
            'range_surface_area': s.range_surface_area,
            'population_minimum_size': s.population_minimum_size,
            'population_maximum_size': s.population_maximum_size,
            'habitat_surface_area': s.habitat_surface_area,
        }
        hist_data.setdefault(code_region, []).append(trend_data)
    return hist_data


def load_habitat_prev(dataset):
    habitats = (
        DataHabitattypeRegion.query
        .join(Dataset)
        .join(DataHabitat)
        .filter(
            Dataset.year_start <= dataset.year_start,
            Dataset.year_end <= dataset.year_end,
        )
        .with_entities(
            Dataset.year_end,
            DataHabitat.code,
            DataHabitattypeRegion.region,
            DataHabitattypeRegion.range_surface_area,
            DataHabitattypeRegion.coverage_surface_area,
        )
    )
    hist_data = {}
    for h in habitats:
        code_region = '{}-{}'.format(h.code, h.region)
        trend_data = {
            'year': h.year_end,
            'range_surface_area': h.range_surface_area,
            'coverage_surface_area': h.coverage_surface_area,
        }
        hist_data.setdefault(code_region, []).append(trend_data)
    return hist_data
