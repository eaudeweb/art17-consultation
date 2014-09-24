from flask.ext.principal import Permission
from flask import render_template
from sqlalchemy import func
from art17.aggregation import aggregation
from art17 import models, ROLE_AGGREGATED, ROLE_DRAFT, ROLE_FINAL
from art17.aggregation.utils import aggregation_missing_data_report
from art17.auth import require, need
from art17.lookup import CONCLUSIONS


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

    def reports(ds):
        ROLE = ROLE_AGGREGATED
        data = {'species': {}, 'habitat': {}}
        for k, v in CONCLUSIONS.iteritems():
            data['species'][k] = (
                ds.species_objs
                .filter_by(cons_role=ROLE, conclusion_assessment=k).count()
            )
            data['habitat'][k] = (
                ds.habitat_objs
                .filter_by(cons_role=ROLE, conclusion_assessment=k).count()
            )
        data['species']['total'] = (
            ds.species_objs.filter_by(cons_role=ROLE).count()
        )
        data['habitat']['total'] = (
            ds.habitat_objs.filter_by(cons_role=ROLE).count()
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
