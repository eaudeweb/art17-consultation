# coding=utf-8
from collections import OrderedDict
from datetime import datetime

from BeautifulSoup import BeautifulSoup
import flask
import requests
from flask import redirect, url_for, render_template, request, current_app, \
    flash
from wtforms import Form, IntegerField, TextField, SelectField
from wtforms.validators import Optional
from flask.ext.principal import Permission

from art17 import dal, models, ROLE_FINAL
from art17.aggregation.forms import CompareForm, PreviewForm
from art17.aggregation.utils import get_checklist, get_reporting_id, \
    get_species_checklist, get_habitat_checklist, valid_checklist
from art17.auth import require, need
from art17.common import perm_fetch_checklist, get_datasets
from art17.models import (
    Dataset,
    DataSpeciesCheckList,
    db,
    DataHabitatsCheckList,
    DATASET_STATUSES_DICT,
    DATASET_STATUSES_LIST,
    LuGrupSpecie,
)
from art17.aggregation import (
    aggregation,
    aggregation_manager,
)
from art17.aggregation.refvalues import (
    load_species_refval,
    refvalue_ok,
    load_habitat_refval,
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


def parse_checklist(checklist_qs):
    result = OrderedDict()
    for item in checklist_qs:
        key = (item.code, item.name)
        if key not in result:
            result[key] = {'info': item, 'regions': [item.bio_region]}
        else:
            result[key]['regions'].append(item.bio_region)
    return result


def parse_checklist_ref(checklist_qs):
    return {(item.code, item.bio_region): item for item in checklist_qs}


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
        year_start=current_app.config.get('DEFAULT_YEAR_START'),
        year_end=current_app.config.get('DEFAULT_YEAR_END'),
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
@require(Permission(need.authenticated))
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
@require(perm_fetch_checklist())
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


class DatasetForm(Form):
    comment = TextField()
    year_start = IntegerField(validators=[Optional()])
    year_end = IntegerField(validators=[Optional()])
    status = SelectField(choices=DATASET_STATUSES_LIST)


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


@aggregation.route('/admin/dataset/<dataset_id>/edit/',
                   methods=('GET', 'POST'))
def edit_dataset(dataset_id):
    dataset = get_datasets().filter_by(id=dataset_id).first()

    if request.method == 'POST':
        form = DatasetForm(request.form, obj=dataset)
        if form.validate():
            form.populate_obj(dataset)
            db.session.commit()
            flash("Form successfully updated", 'success')
        else:
            flash("Form has errors", 'error')
    else:
        form = DatasetForm(obj=dataset)

    return render_template(
        'aggregation/admin/edit_dataset.html',
        page='checklist',
        dataset=dataset,
        form=form,
    )


@aggregation.route('/admin/reference_values')
def reference_values():
    checklist_id = get_reporting_id()
    current_checklist = get_checklist(checklist_id)
    checklist_id = current_checklist.id

    species_refvals = load_species_refval()
    species_checklist = get_species_checklist(dataset_id=checklist_id)
    species_data = parse_checklist_ref(species_checklist)

    species_list = get_species_checklist(groupped=True,
                                         dataset_id=checklist_id)

    habitat_refvals = load_habitat_refval()
    habitat_checklist = get_habitat_checklist(dataset_id=checklist_id)
    habitat_data = parse_checklist_ref(habitat_checklist)
    habitat_list = get_habitat_checklist(distinct=True,
                                         dataset_id=checklist_id,
                                         groupped=True)
    relevant_regions = (
        {s.bio_region for s in species_checklist}.union(
            {h.bio_region for h in habitat_checklist}
        ))
    bioreg_list = dal.get_biogeo_region_list(relevant_regions)

    groups = dict(
        LuGrupSpecie.query
        .with_entities(LuGrupSpecie.code, LuGrupSpecie.description)
    )

    return render_template(
        'aggregation/admin/reference_values.html',
        species_refvals=species_refvals,
        species_data=species_data,
        species_list=species_list,
        habitat_refvals=habitat_refvals,
        habitat_data=habitat_data,
        habitat_list=habitat_list,
        bioreg_list=bioreg_list,
        GROUPS=groups,
        current_checklist=current_checklist,
        page='refvalues',
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
    return {
        'checklists': get_checklists(),
        'datasets': get_datasets(),
        'DATASET_STATUSES': DATASET_STATUSES_DICT,
        'refvalue_ok': refvalue_ok,
    }


@aggregation.route('/admin/compare/select', methods=('GET', 'POST'))
def compare():
    if request.method == 'POST':
        form = CompareForm(request.form)

        if form.validate():
            return flask.redirect(
                flask.url_for(
                    '.compare_datasets',
                    dataset1=form.dataset1.data,
                    dataset2=form.dataset2.data)
            )
    else:
        form = CompareForm()
    return flask.render_template('aggregation/compare.html', form=form,
                                 page='compare')


@aggregation.route('/admin/compare/<int:dataset1>/<int:dataset2>/')
def compare_datasets(dataset1, dataset2):
    d1 = models.Dataset.query.get_or_404(dataset1)
    d2 = models.Dataset.query.get_or_404(dataset2)

    conclusions_s_d1 = d1.species_objs.filter_by(cons_role=ROLE_FINAL)
    conclusions_s_d2 = d2.species_objs.filter_by(cons_role=ROLE_FINAL)

    relevant_regions = set([r[0] for r in (
        list(conclusions_s_d1.with_entities(models.DataSpeciesRegion.region)
             .distinct()) +
        list(conclusions_s_d2.with_entities(models.DataSpeciesRegion.region)
             .distinct())
    ) if r[0]])

    s_data = {}
    for r in conclusions_s_d1:
        if r.species not in s_data:
            s_data[r.species] = {'d1': {}, 'd2': {}}
        s_data[r.species]['d1'][r.region] = r
    for r in conclusions_s_d2:
        if r.species not in s_data:
            s_data[r.species] = {'d1': {}, 'd2': {}}
        s_data[r.species]['d2'][r.region] = r
    if None in s_data:
        del s_data[None]

    s_stat = {'objs': 0, 'diff': 0}
    for k, v in s_data.iteritems():
        for reg, ass in v['d1'].iteritems():
            ass2 = v['d2'].get(reg, None)
            if not ass2 or ass2.conclusion_assessment != ass.conclusion_assessment:
                s_stat['diff'] += 1
            s_stat['objs'] += 1

    conclusions_h_d1 = d1.habitat_objs.filter_by(cons_role=ROLE_FINAL)
    conclusions_h_d2 = d2.habitat_objs.filter_by(cons_role=ROLE_FINAL)

    h_data = {}
    for r in conclusions_h_d1:
        if r.habitat not in h_data:
            h_data[r.habitat] = {'d1': {}, 'd2': {}}
        h_data[r.habitat]['d1'][r.region] = r
    for r in conclusions_h_d2:
        if r.habitat not in h_data:
            h_data[r.habitat] = {'d1': {}, 'd2': {}}
        h_data[r.habitat]['d2'][r.region] = r
    if None in h_data:
        del h_data[None]

    h_stat = {'objs': 0, 'diff': 0}
    for k, v in h_data.iteritems():
        for reg, ass in v['d1'].iteritems():
            ass2 = v['d2'].get(reg, None)
            if not ass2 or ass2.conclusion_assessment != ass.conclusion_assessment:
                h_stat['diff'] += 1
            h_stat['objs'] += 1

    bioreg_list = dal.get_biogeo_region_list(relevant_regions)
    return render_template(
        'aggregation/compare_datasets.html',
        species_data=s_data, dataset1=d1, dataset2=d2, bioreg_list=bioreg_list,
        habitat_data=h_data, s_stat=s_stat, h_stat=h_stat,
        page='compare',
    )


@aggregation.route('/manage/reference_values/')
@aggregation.route('/manage/reference_values/<page>', methods=['GET', 'POST'])
def manage_refvals(page='habitat'):
    current_checklist = valid_checklist()
    checklist_id = current_checklist.id

    dataset = None
    form = PreviewForm(formdata=request.form, page=page,
                       checklist_id=checklist_id)
    report = None
    return flask.render_template(
        'aggregation/manage/refvals_start.html',
        **{
            'form': form, 'dataset': dataset, 'report': report, 'page': page,
            'current_checklist': current_checklist,
            'endpoint': '.manage_refvals',
        })
