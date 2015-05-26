# coding=utf-8
from collections import OrderedDict

import flask
from flask import redirect, url_for, render_template, request, flash, Response
from wtforms import Form, IntegerField, TextField, SelectField
from wtforms.validators import Optional
from flask.ext.principal import Permission
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from art17 import dal, models, ROLE_FINAL
from art17.aggregation.checklist import create_checklist
from art17.aggregation.forms import CompareForm, PreviewForm
from art17.aggregation.utils import (
    get_checklist, get_reporting_id, get_species_checklist,
    get_habitat_checklist, valid_checklist, sum_of_reports,
)
from art17.auth import require, need
from art17.common import get_datasets, TemplateView
from art17.models import (
    Dataset,
    db,
    DATASET_STATUSES_DICT,
    DATASET_STATUSES_LIST,
    LuGrupSpecie,
)
from art17.aggregation import (
    aggregation,
    perm_edit_refvals,
    perm_view_refvals,
    MIMETYPE)
from art17.aggregation.refvalues import (
    load_species_refval,
    refvalue_ok,
    load_habitat_refval,
    get_subject_refvals, get_subject_refvals_wip, set_subject_refvals_wip,
    get_subject_refvals_mixed,
)

REGIONS = {
    'ALP': 'Alpina',
    'CON': 'Continentala',
    'PAN': 'Panonica',
    'STE': 'Stepica',
    'BLS': 'Boreala',
    'MBLS': 'Marea Neagra',
}


def get_checklists():
    return Dataset.query.filter_by(checklist=True).order_by(Dataset.date.desc())


def parse_checklist(checklist_qs):
    result = OrderedDict()
    for item in checklist_qs:
        key = (item.code, item.name)
        if key not in result:
            result[key] = {'info': item, 'regions': [item.bio_region]}
        else:
            result[key]['regions'].append(item.bio_region)
    return result


@aggregation.route('/admin/')
@require(Permission(need.admin))
def admin():
    return redirect(url_for('.checklists'))


@aggregation.route('/admin/checklists/')
@require(Permission(need.admin))
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
@require(Permission(need.admin))
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
@require(Permission(need.admin))
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


class DatasetForm(Form):
    comment = TextField()
    year_start = IntegerField(validators=[Optional()])
    year_end = IntegerField(validators=[Optional()])
    status = SelectField(choices=DATASET_STATUSES_LIST)
    checklist_id = SelectField(validators=[Optional()], choices=[])

    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.checklist_id.choices = (
            [('', u'Lista de verificare inițială')] +
            [(unicode(c.id), unicode(c)) for c in get_checklists()]
        )


@aggregation.route('/admin/checklist/<dataset_id>/edit/',
                   methods=('GET', 'POST'))
@require(Permission(need.admin))
def edit_checklist(dataset_id):
    dataset = get_checklists().filter_by(id=dataset_id).first()

    if request.method == 'POST':
        form = ChecklistForm(request.form, obj=dataset)
        if form.validate():
            form.populate_obj(dataset)
            db.session.commit()
            return redirect(url_for('.admin'))
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
@require(Permission(need.admin))
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


class ReferenceValues(TemplateView):
    template_name = 'aggregation/admin/reference_values.html'
    decorators = [require(Permission(need.admin))]

    def get_context(self, **kwargs):
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

        return dict(
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


aggregation.add_url_rule('/admin/reference_values',
                         view_func=ReferenceValues.as_view('reference_values'))


@aggregation.app_context_processor
def inject_globals():
    return {
        'checklists': get_checklists(),
        'datasets': get_datasets(),
        'DATASET_STATUSES': DATASET_STATUSES_DICT,
        'refvalue_ok': refvalue_ok,
        'sum_of_reports': sum_of_reports,
    }


@aggregation.route('/admin/compare/select', methods=('GET', 'POST'))
@require(Permission(need.admin))
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
@require(Permission(need.admin))
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


@aggregation.route('/manage/reference_values/', methods=['GET', 'POST'])
@aggregation.route('/manage/reference_values/<page>', methods=['GET', 'POST'])
@require(perm_edit_refvals())
def manage_refvals(page='habitat'):
    current_checklist = valid_checklist()
    checklist_id = current_checklist.id

    dataset = None
    form = PreviewForm(formdata=request.form, page=page,
                       checklist_id=checklist_id)
    report = None
    if request.method == 'POST':
        if form.validate():
            subject = form.subject.data
            return redirect(
                url_for('.manage_refvals_form', page=page, subject=subject))
    return flask.render_template(
        'aggregation/manage/refvals_start.html',
        **{
            'form': form, 'dataset': dataset, 'report': report, 'page': page,
            'current_checklist': current_checklist,
            'endpoint': '.manage_refvals',
        })


class ManageReferenceValues(ReferenceValues):
    template_name = 'aggregation/manage/reference_values.html'
    decorators = [require(perm_view_refvals())]


aggregation.add_url_rule('/manage/reference_values/table',
                         view_func=ManageReferenceValues.as_view(
                             'manage_refvals_table'))


@aggregation.route('/manage/reference_values/<page>/form/<subject>',
                   methods=['GET', 'POST'])
@require(perm_edit_refvals())
def manage_refvals_form(page, subject):
    data = get_subject_refvals(page, subject)

    if request.method == "POST":
        set_subject_refvals_wip(page, subject, request.form)
        flask.flash(u"Valori actualizate", 'success')

    extra = get_subject_refvals_wip(page, subject)
    full = get_subject_refvals_mixed(page, subject)
    checklist_id = get_reporting_id()
    current_checklist = get_checklist(checklist_id)
    checklist_id = current_checklist.id
    if page == 'habitat':
        names = get_habitat_checklist(distinct=True, dataset_id=checklist_id)
    elif page == 'species':
        names = get_species_checklist(distinct=True, dataset_id=checklist_id)
    name_and_code = names.filter_by(code=subject).first()[1]
    _, _, name = name_and_code.partition(subject)

    return flask.render_template(
        'aggregation/manage/refvals_form.html', page=page, subject=subject,
        data=data, extra=extra, full=full, name=name, REGIONS=REGIONS,
    )


@aggregation.route('/manage/reference_values/<page>/form/<subject>/download',
                   methods=['GET'])
def download_refvals(page, subject):
    REFGROUPS = {
        'range': 'Areal',
        'magnitude': 'Magnitudine Areal',
        'population_units': 'Unitati populatie',
        'population_magnitude': 'Magnitudine Populatie',
        'population_range': 'Areal favorabil populatie',
        'coverage_range': 'Suprafata',
        'coverage_magnitude': 'Magnitudine suprafata',
    }
    checklist_id = get_reporting_id()
    current_checklist = get_checklist(checklist_id)
    checklist_id = current_checklist.id
    if page == 'habitat':
        names = get_habitat_checklist(distinct=True, dataset_id=checklist_id)
    elif page == 'species':
        names = get_species_checklist(distinct=True, dataset_id=checklist_id)
    else:
        raise NotImplementedError()
    name_and_code = names.filter_by(code=subject).first()[1]
    _, _, name = name_and_code.partition(subject)
    full = get_subject_refvals_mixed(page, subject)

    changed_dict = {}
    for (region, d1) in full.items():
        for (sheet_name, d2) in d1.items():
            if sheet_name not in changed_dict.keys():
                changed_dict[sheet_name] = {}
            changed_dict[sheet_name][region] = d2

    wb = Workbook()
    wb.remove_sheet(wb.get_sheet_by_name('Sheet'))

    for (sheet_name, d1) in changed_dict.items():
        ws = wb.create_sheet()
        ws.title = REFGROUPS.get(sheet_name, sheet_name.title())
        operators = d1.values()[0].keys()
        ws.append(['COD SPECIE', 'NUME', 'BIOREGIUNE'] + operators)
        for (bioregion, d2) in d1.items():
            ws.append([subject, name, bioregion] +
                      [d2.get(operator) for operator in operators])

    response = Response(save_virtual_workbook(wb), mimetype=MIMETYPE)
    response.headers.add('Content-Disposition',
                         'attachment; filename={}.xlsx'.format(subject))
    return response


def parse_checklist_ref(checklist_qs):
    return {(item.code, item.bio_region): item for item in checklist_qs}
