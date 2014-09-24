from flask.ext.principal import Permission
from flask import render_template
from sqlalchemy import func
from art17.aggregation import aggregation
from art17 import models, ROLE_AGGREGATED, ROLE_DRAFT, ROLE_FINAL
from art17.aggregation.utils import aggregation_missing_data_report
from art17.auth import require, need
from art17.lookup import CONCLUSIONS

PRESSURES = {
    'A': 'Agricultura',
    'B': 'Silvicultura',
    'C': 'Minerit, extractia de materiale si de productie de energie',
    'D': 'Retele de comunicatii',
    'E': 'Urbanizare, dezvoltare rezidentiala si comerciala',
    'F': 'Folosirea resurselor biologice, altele decat agricultura si silvicultura',
    'G': 'Intruziuni si dezechilibre umane',
    'H': 'Poluare',
    'I': 'Specii invazive, alte probleme ale speciilor si genele',
    'J': 'Modificari ale sistemului natural',
    'K': 'Procesele naturale biotice si abiotice (fara catastrofe)',
    'L': 'Evenimente geologice, catastrofe nturale',
    'M': 'Schimbari globale',
    'U': 'presiuni si amenintari necunoscute',
}


def get_report_data(dataset):
    species = dataset.species_objs.filter(
        models.DataSpeciesRegion.cons_role.in_(
            (ROLE_AGGREGATED, ROLE_DRAFT, ROLE_FINAL)))
    habitats = dataset.habitat_objs.filter(
        models.DataHabitattypeRegion.cons_role.in_(
            (ROLE_AGGREGATED, ROLE_DRAFT, ROLE_FINAL)))
    return species, habitats


@aggregation.route('/raport/<int:dataset_id>')
@require(Permission(need.authenticated))
def report(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)

    species, habitats = get_report_data(dataset)

    def reports(ds):
        data = {'species': {}, 'habitat': {}}
        for k, v in CONCLUSIONS.iteritems():
            data['species'][k] = (
                species
                .filter_by(conclusion_assessment=k).count()
            )
            data['habitat'][k] = (
                habitats
                .filter_by(conclusion_assessment=k).count()
            )
        data['species']['total'] = (
            species.count()
        )
        data['habitat']['total'] = (
            habitats.count()
        )

        data['species']['total_species'] = (
            models.DataSpeciesCheckList.query
            .with_entities(
                func.count(models.DataSpeciesCheckList.species_name))
            .filter_by(dataset_id=ds.checklist_id)
            .group_by(models.DataSpeciesCheckList.species_name).count())

        queryset = data['species']['total_reports'] = (
            models.DataSpeciesCheckList.query
            .filter_by(dataset_id=ds.checklist_id).count()
        )

        data['habitat']['total_habitats'] = (
            models.DataHabitatsCheckList.query
            .with_entities(func.count(models.DataHabitatsCheckList.valid_name))
            .filter_by(dataset_id=ds.checklist_id)
            .group_by(models.DataHabitatsCheckList.valid_name).count())

        queryset = data['habitat']['total_reports'] = (
            models.DataHabitatsCheckList.query
            .filter_by(dataset_id=ds.checklist_id).count()
        )

        data['missing'] = aggregation_missing_data_report(dataset_id)
        return data

    dataset.reports = reports(dataset)
    return render_template('aggregation/reports/report.html',
                           dataset=dataset,
                           dataset_id=dataset.id)


@aggregation.route('/raport/<int:dataset_id>/conservation_status')
@require(Permission(need.authenticated))
def report_conservation_status(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)
    species, habitats = get_report_data(dataset)
    species = list(species)
    habitats = list(habitats)
    all_species = len(species) or 1
    all_habitats = len(habitats) or 1
    stats = {
        'species': {'range': {}, 'population': {}, 'habitat': {}, 'future': {},
                    'assessment': {}},
        'habitats': {'range': {}, 'area': {}, 'structure': {}, 'future': {},
                     'assessment': {}}
    }

    def set_stat(conclusion, stats):
        conclusion = conclusion or '-'
        stats.setdefault(conclusion, 0)
        stats[conclusion] += 1

    for spec in species:
        set_stat(spec.conclusion_range, stats['species']['range'])
        set_stat(spec.conclusion_population, stats['species']['population'])
        set_stat(spec.conclusion_habitat, stats['species']['habitat'])
        set_stat(spec.conclusion_future, stats['species']['future'])
        set_stat(spec.conclusion_assessment, stats['species']['assessment'])
    for hab in habitats:
        set_stat(hab.conclusion_range, stats['habitats']['range'])
        set_stat(hab.conclusion_area, stats['habitats']['area'])
        set_stat(hab.conclusion_structure, stats['habitats']['structure'])
        set_stat(hab.conclusion_future, stats['habitats']['future'])
        set_stat(hab.conclusion_assessment, stats['habitats']['assessment'])
    for k, values in stats['species'].iteritems():
        for conclusion, v in values.iteritems():
            stats['species'][k][conclusion] = v * 100.0 / all_species
    for k, values in stats['habitats'].iteritems():
        for conclusion, v in values.iteritems():
            stats['habitats'][k][conclusion] = v * 100.0 / all_habitats

    return render_template(
        'aggregation/reports/conservation_status.html',
        dataset=dataset, dataset_id=dataset.id,
        species=species, habitats=habitats, page='conservation', stats=stats)


@aggregation.route('/raport/<int:dataset_id>/bioreg_global')
@require(Permission(need.authenticated))
def report_bioreg_global(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)
    species, habitats = get_report_data(dataset)

    all_species = species.count()
    all_habitats = habitats.count()

    REGIONS = ('ALP', 'CON', 'PAN', 'STE', 'BLS', 'MBLS')
    stats = {
        'species': {r: {} for r in REGIONS},
        'habitats': {r: {} for r in REGIONS}
    }

    for spec in species:
        conclusion = spec.conclusion_assessment or 'NA'
        stats['species'].setdefault(spec.region, {})
        stats['species'][spec.region].setdefault(conclusion, 0)
        stats['species'][spec.region][conclusion] += 1

    for hab in habitats:
        conclusion = hab.conclusion_assessment or 'NA'
        stats['habitats'].setdefault(hab.region, {})
        stats['habitats'][hab.region].setdefault(conclusion, 0)
        stats['habitats'][hab.region][conclusion] += 1

    for k, values in stats['species'].iteritems():
        for conclusion, v in values.iteritems():
            all_species = sum(stats['species'][k].values()) or 1
            stats['species'][k][conclusion] = v * 100.0 / all_species
    for k, values in stats['habitats'].iteritems():
        for conclusion, v in values.iteritems():
            all_habitats = sum(stats['habitats'][k].values()) or 1
            stats['habitats'][k][conclusion] = v * 100.0 / all_habitats

    return render_template(
        'aggregation/reports/bioreg_global.html',
        dataset=dataset, dataset_id=dataset.id, regions=REGIONS,
        species=species, habitats=habitats, page='bioreg', stats=stats)


@aggregation.route('/raport/<int:dataset_id>/pressures1')
def report_pressures1(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)
    species, habitats = get_report_data(dataset)

    species_pres = (
        species.join(models.DataPressuresThreats)
        .filter(models.DataPressuresThreats.type == 'p')
        .with_entities(models.DataPressuresThreats.pressure,
                       func.count(models.DataPressuresThreats.id))
        .group_by(models.DataPressuresThreats.pressure,
                  models.DataPressuresThreats.type)
    ).all()
    species_thr = (
        species.join(models.DataPressuresThreats)
        .filter(models.DataPressuresThreats.type == 't')
        .with_entities(models.DataPressuresThreats.pressure,
                       func.count(models.DataPressuresThreats.id))
        .group_by(models.DataPressuresThreats.pressure,
                  models.DataPressuresThreats.type)
    ).all()
    habitat_pres = (
        habitats.join(models.DataPressuresThreats)
        .filter(models.DataPressuresThreats.type == 'p')
        .with_entities(models.DataPressuresThreats.pressure,
                       func.count(models.DataPressuresThreats.id))
        .group_by(models.DataPressuresThreats.pressure)
    ).all()
    habitat_thr = (
        habitats.join(models.DataPressuresThreats)
        .filter(models.DataPressuresThreats.type == 't')
        .with_entities(models.DataPressuresThreats.pressure,
                       func.count(models.DataPressuresThreats.id))
        .group_by(models.DataPressuresThreats.pressure)
    ).all()

    stats = {}
    for k in PRESSURES:
        stats.setdefault(k, {})
        stats[k].setdefault('species', {})
        stats[k]['species']['pressures'] = sum(
            [val for name, val in species_pres if name and name.startswith(k)])
        stats[k]['species']['threats'] = sum(
            [val for name, val in species_thr if name and name.startswith(k)])
        stats[k].setdefault('habitats', {})
        stats[k]['habitats']['pressures'] = sum(
            [val for name, val in habitat_pres if name and name.startswith(k)])
        stats[k]['habitats']['threats'] = sum(
            [val for name, val in habitat_thr if name and name.startswith(k)])
    all_spec_pres = sum([stats[k]['species']['pressures'] for k in PRESSURES]) or 1
    all_spec_thr = sum([stats[k]['species']['threats'] for k in PRESSURES]) or 1
    all_hab_pres = sum([stats[k]['habitats']['pressures'] for k in PRESSURES]) or 1
    all_hab_thr = sum([stats[k]['habitats']['threats'] for k in PRESSURES]) or 1
    for k in PRESSURES:
        stats[k]['species']['pressures'] = stats[k]['species']['pressures'] * 100.0 / all_spec_pres
        stats[k]['species']['threats'] = stats[k]['species']['threats'] * 100.0 / all_spec_thr
        stats[k]['habitats']['pressures'] = stats[k]['habitats']['pressures'] * 100.0 / all_hab_pres
        stats[k]['habitats']['threats'] = stats[k]['habitats']['threats'] * 100.0 / all_hab_thr

    return render_template(
        'aggregation/reports/pressures1.html',
        dataset=dataset, dataset_id=dataset.id, pressures=PRESSURES,
        species=species, habitats=habitats, page='pressures1', stats=stats)
