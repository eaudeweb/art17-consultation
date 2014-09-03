import flask
from art17 import models
from art17.scripts import exporter


DEFAULT_DATASET_ID=1


@exporter.command
def xml_species(filename=None, dataset_id=None):
    dataset_id = dataset_id or DEFAULT_DATASET_ID
    species = models.db.session.query(models.DataSpecies)
    data = flask.render_template(
                'xml_export/species.html',
                **{'species_list': species, 'dataset_id': dataset_id}
            )
    if filename:
        with open(filename, 'w') as file_out:
            file_out.write(data.encode('utf-8'))
    return data


@exporter.command
def xml_species_checklist(filename=None):
    species = models.db.session.query(
                    models.DataSpeciesCheckList).filter_by(
                            member_state='RO')

    species_as_dict = {}
    for sp in species:
        try:
            species_as_dict[sp.code]['regions'].append(sp)
        except KeyError:
            species_as_dict[sp.code] = {
                        'info': sp,
                        'regions': [sp],
                    }

    data = flask.render_template(
                'xml_export/species_checklist.html',
                **{'species_dict': species_as_dict}
            )

    if filename:
        with open(filename, 'w') as file_out:
            file_out.write(data.encode('utf-8'))
    return data


@exporter.command
def xml_habitats(filename=None, dataset_id=None):
    dataset_id = dataset_id or DEFAULT_DATASET_ID
    habitats = models.db.session.query(models.DataHabitat)
    data = flask.render_template(
                'xml_export/habitats.html',
                **{'habitats': habitats, 'dataset_id': dataset_id}
            )
    if filename:
        with open(filename, 'w') as file_out:
            file_out.write(data.encode('utf-8'))
    return data


@exporter.command
def xml_habitats_checklist(filename=None):
    habitats = models.db.session.query(
                    models.DataHabitatsCheckList).filter_by(
                            member_state='RO')

    habitats_as_dict = {}
    for hb in habitats:
        try:
            habitats_as_dict[hb.code]['regions'].append(hb)
        except KeyError:
            habitats_as_dict[hb.code] = {
                        'info': hb,
                        'regions': [hb],
                    }

    data = flask.render_template(
                'xml_export/habitats_checklist.html',
                **{'habitats_dict': habitats_as_dict}
            )

    if filename:
        with open(filename, 'w') as file_out:
            file_out.write(data.encode('utf-8'))
    return data
