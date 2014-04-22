from collections import OrderedDict
from datetime import datetime
from BeautifulSoup import BeautifulSoup
import requests
from flask import redirect, url_for, render_template, request, current_app
from wtforms import Form, IntegerField, TextField
from wtforms.validators import Optional

from art17.aggregation import (
    aggregation,
    aggregation_manager,
    get_species_checklist,
    get_habitat_checklist,
)
from art17.models import (
    Dataset,
    DataSpeciesCheckList,
    db,
    DataHabitatsCheckList,
)


REGION_MAP = {
    'Panonica': 'PAN',
    'Alpina': 'ALP',
    'Continentala': 'CON',
    'Stepica': 'STE',
    'Mediteraneana': 'MED',
    'Boreala': 'BOR',
    'Marea Neagra': 'MBLS',
    'Pontic': 'BLS',
}

PRESENCE_MAP = {
    'Prezent': '1',
    'Rezerva stiintifica': 'SR',
    'Reintrodus': '1',
    'Extinct': 'EXB',
    'Extinct in salbaticie': 'EXB',
    'Marginal': 'MAR',
}


def get_checklists():
    return Dataset.query.filter_by(checklist=True)


def parse_checklist(list):
    result = OrderedDict()
    for item in list:
        key = (item.code, item.name)
        if key not in result:
            result[key] = {'info': item, 'regions': [item.bio_region]}
        else:
            result[key]['regions'].append(item.bio_region)
    return result


def species_from_oid(data, dataset):
    b = BeautifulSoup(data)
    entries = b.findAll("entry")

    species = []
    for e in entries:
        cod_specie = e.content.findAll("d:codspecie")[0].text
        name = e.content.findAll("d:denumirestiintifica")[0].text
        region = e.content.findAll("d:bioregiune")[0].text
        presence = e.content.findAll("d:statusverificare")[0].text
        guid = e.content.findAll("d:id")[0].text
        if region not in REGION_MAP:
            raise ValueError('Unknown region: ' + region)
        region = REGION_MAP[region]
        if presence not in PRESENCE_MAP:
            raise ValueError('Unknown presence: ' + presence)
        presence = PRESENCE_MAP[presence]
        data = {
            'code': cod_specie, 'name': name, 'bio_region': region,
            'presence': presence, 'globalid': guid,
            'hd_name': name,
            'member_state': 'RO',
        }
        if dataset:
            data['dataset_id'] = dataset.id
            species.append(DataSpeciesCheckList(**data))
        else:
            species.append(data)
    return species


def habitats_from_oid(data, dataset):
    b = BeautifulSoup(data)
    entries = b.findAll("entry")

    habitats = []
    for e in entries:
        cod = e.content.findAll("d:codhabitat")[0].text
        name = e.content.findAll("d:numehabitat")[0].text
        region = e.content.findAll("d:bioregiune")[0].text
        presence = e.content.findAll("d:statusverificare")[0].text
        guid = e.content.findAll("d:id")[0].text
        if region not in REGION_MAP:
            raise ValueError('Unknown region: ' + region)
        region = REGION_MAP[region]
        if presence not in PRESENCE_MAP:
            raise ValueError('Unknown presence: ' + presence)
        presence = PRESENCE_MAP[presence]
        data = {
            'code': cod, 'name': name, 'bio_region': region,
            'presence': presence, 'globalid': guid,
            'member_state': 'RO',
        }
        if dataset:
            data['dataset_id'] = dataset.id
            habitats.append(DataHabitatsCheckList(**data))
        else:
            habitats.append(data)
    return habitats


def create_checklist():
    species_endpoint = current_app.config.get(
        'OID_SPECIES',
        'http://natura.anpm.ro/api/CNSERVICE.svc/ListaVerificareSpecii',
    )
    habitats_endpoint = current_app.config.get(
        'OID_HABITATS',
        'http://natura.anpm.ro/api/CNSERVICE.svc/ListaVerificareHabitate',
    )
    dataset = Dataset(
        preview=True, checklist=True, date=datetime.today(),
        comment=str(datetime.now()),
    )
    db.session.add(dataset)
    db.session.commit()

    response = requests.get(species_endpoint)
    species = species_from_oid(response.content, dataset)

    response = requests.get(habitats_endpoint)
    habitats = habitats_from_oid(response.content, dataset)

    for o in species + habitats:
        db.session.add(o)
    db.session.commit()


@aggregation.route('/admin/')
def admin():
    return redirect(url_for('.checklists'))


@aggregation.route('/admin/checklists/')
def checklists():
    checklists = get_checklists()

    default_checklist = {
        'species_checklist': get_species_checklist().all(),
        'habitat_checklist': get_habitat_checklist().all(),
    }
    return render_template(
        'aggregation/admin/checklists.html',
        page='checklist',
        default_list=default_checklist,
        checklists=checklists,
    )


@aggregation.route('/admin/checklist/initial/')
@aggregation.route('/admin/checklist/<dataset_id>/')
def checklist(dataset_id=None):
    species = get_species_checklist(dataset_id=dataset_id)
    habitats = get_habitat_checklist(dataset_id=dataset_id)
    species_dict = parse_checklist(species)
    habitats_dict = parse_checklist(habitats)

    return render_template(
        'aggregation/admin/checklist.html',
        species_dict=species_dict,
        habitats_dict=habitats_dict,
        page='checklist',
    )


@aggregation.route('/admin/checklist/create/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        create_checklist()
        return redirect(url_for('.checklists'))
    return render_template(
        'aggregation/admin/checklist_create.html',
        page='checklist',
    )


class ChecklistForm(Form):
    comment = TextField()
    year_start = IntegerField(validators=[Optional()])
    year_end = IntegerField(validators=[Optional()])


@aggregation.route('/admin/checklist/<dataset_id>/edit/',
                   methods=('GET', 'POST'))
def edit_checklist(dataset_id):
    dataset = get_checklists().filter_by(id=dataset_id).first()

    if request.method == 'POST':
        form = ChecklistForm(request.form, obj=dataset)
        if form.validate():
            form.populate_obj(dataset)
            db.session.commit()
    else:
        form = ChecklistForm(obj=dataset)

    return render_template(
      'aggregation/admin/edit_checklist.html',
      page='checklist',
      dataset=dataset,
      form=form,
    )


@aggregation_manager.command
def checklist():
    with open('misc/ListaVerificareHabitate.xml') as fin:
        habitats = habitats_from_oid(fin, None)
        print "Habitat:", habitats[0] if habitats else '-'
    with open('misc/ListaVerificareSpecii.xml') as fin:
        species = species_from_oid(fin, None)
        print "Specie:", species[0] if species else '-'


@aggregation.app_context_processor
def inject_globals():
    return {'checklists': get_checklists()}
