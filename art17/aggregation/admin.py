from collections import OrderedDict
from flask import redirect, url_for, render_template
from art17.aggregation import (
    aggregation,
    get_species_checklist,
    get_habitat_checklist,
)
from art17.models import Dataset


def parse_checklist(list):
    result = OrderedDict()
    for item in list:
        key = (item.code, item.name)
        if key not in result:
            result[key] = [item.bio_region]
        else:
            result[key].append(item.bio_region)
    return result


@aggregation.route('/admin/')
def admin():
    return redirect(url_for('config.form'))


@aggregation.route('/admin/checklists/')
def checklists():
    checklists = Dataset.query.filter_by(checklist=True).all()

    return render_template('aggregation/admin/checklists.html',
                           page='checklist',
                           checklists=checklists)


@aggregation.route('/admin/checklist/initial/')
@aggregation.route('/admin/checklist/<id>/')
def checklist(id=None):
    if id is None:
        species = get_species_checklist()
        habitats = get_habitat_checklist()
    else:
        raise NotImplementedError()
    species_dict = parse_checklist(species)
    habitats_dict = parse_checklist(habitats)

    return render_template(
        'aggregation/admin/checklist.html',
        species_dict=species_dict,
        habitats_dict=habitats_dict,
    )
