# encoding: utf-8
from datetime import datetime

import flask
from flask import request, redirect, url_for
from flask.ext.principal import Permission
from flask.views import View
from sqlalchemy import func, or_
from werkzeug.datastructures import MultiDict

from art17 import models, forms, schemas, dal
from art17.auth import admin_permission, require, need
from art17.common import (
    flatten_dict,
    FINALIZED_STATUS,
    NEW_STATUS,
    perm_aggregate_dataset,
)
from art17.habitat import (
    detail as detail_habitat,
    HabitatCommentView,
    get_dal as get_habitat_dal,
)
from art17.lookup import CONCLUSIONS
from art17.species import (
    detail as detail_species,
    SpeciesCommentView,
    get_dal as get_species_dal,
)
from art17.aggregation import (
    aggregation,
    check_aggregation_perm,
    perm_edit_record,
    perm_finalize_record,
    perm_definalize_record,
    check_aggregation_preview_perm,
    load_species_refval, load_habitat_refval)
from art17.aggregation.agregator import (
    create_aggregation,
    create_preview_aggregation,
)
from art17.common import get_datasets
from art17.aggregation.forms import PreviewForm
from art17.aggregation.utils import (
    record_edit_url,
    record_details_url,
    record_finalize_toggle_url,
    aggregation_missing_data_report,
    get_species_checklist, get_habitat_checklist, get_tabmenu_data,
    get_tabmenu_preview,
    valid_checklist,
)


@aggregation.route('/_ping')
def ping():
    from art17 import models
    from datetime import datetime

    count = models.History.query.count()
    now = datetime.utcnow().isoformat()
    return "art17 aggregation is up; %s; %d history items" % (now, count)


@aggregation.route('/_crashme')
def crashme():
    raise RuntimeError("Crashing, as requested.")


@aggregation.route('/')
def home():
    check_aggregation_perm()
    preview_list = (
        models.Dataset.query
        .filter_by(preview=True, user_id=flask.g.identity.id)
        .filter(or_(models.Dataset.checklist == None,
                    models.Dataset.checklist == False))
        .order_by(models.Dataset.date)
        .all()
    )
    return flask.render_template('aggregation/home.html', **{
        'preview_datasets': preview_list,
    })


@aggregation.route('/executa_agregare', methods=['GET', 'POST'])
@require(perm_aggregate_dataset())
def aggregate():
    check_aggregation_perm()
    if request.method == 'POST':
        report, dataset = create_aggregation(
            datetime.utcnow(),
            flask.g.identity.id,
        )
        models.db.session.commit()

    else:
        report = None
        dataset = None

    return flask.render_template('aggregation/aggregate.html', **{
        'report': report,
        'dataset': dataset,
    })


@aggregation.route('/previzualizare/<page>/', methods=['GET', 'POST'])
def preview(page):
    current_checklist = valid_checklist()
    check_aggregation_preview_perm()
    if page == 'habitat':
        qs = list(get_habitat_checklist(distinct=True))
        qs_dict = dict(qs)
    elif page == 'species':
        orig_qs = list(get_species_checklist(distinct=True))
        qs_dict = dict(orig_qs)

        orig_qs = {a[0]: a for a in orig_qs}
        qs = []
        for group in models.LuGrupSpecie.query.all():
            species = (
                models.LuHdSpecies.query
                .filter_by(group_code=group.code)
                .order_by(models.LuHdSpecies.speciesname)
            )
            species = [
                orig_qs[str(s.code)]
                for s in species if str(s.code) in orig_qs
            ]
            qs.append((group.description, species))
    else:
        raise NotImplementedError()

    report = None
    dataset = None
    form = PreviewForm(request.form)
    form.subject.choices = qs
    if request.method == "POST":
        if form.validate():
            report, dataset = create_preview_aggregation(
                page,
                form.subject.data,
                qs_dict.get(form.subject.data),
                datetime.utcnow(),
                flask.g.identity.id,
            )
            models.db.session.commit()
            return redirect(url_for('.post_preview', dataset_id=dataset.id))
        else:
            flask.flash('Invalid form', 'error')
    return flask.render_template('aggregation/preview/preview.html', **{
        'form': form,
        'dataset': dataset,
        'report': report,
        'page': page,
        'current_checklist': current_checklist,
    })


@aggregation.route('/previzualizare/redo/<int:dataset_id>')
@admin_permission.require()
def redo(dataset_id):
    """ Redo a preview aggregation """
    dataset = (
        models.Dataset.query
        .filter_by(preview=True, id=dataset_id).first_or_404()
    )

    species = dataset.species_objs.first()
    habitat = dataset.habitat_objs.first()

    if not any((species, habitat)):
        flask.abort(404)

    page = 'species' if species else 'habitat'
    subject = species.subject if species else habitat.subject
    subject = subject.code

    report, dataset = create_preview_aggregation(
        page,
        subject,
        dataset.comment,
        datetime.utcnow(),
        flask.g.identity.id,
    )
    models.db.session.commit()
    delete_dataset(dataset_id)
    flask.flash(u'O nouă agregare a fost rulată', 'success')
    return redirect(url_for('.post_preview', dataset_id=dataset.id))


@aggregation.route('/sterge/<int:dataset_id>', methods=['POST'])
@admin_permission.require()
def delete_dataset(dataset_id):
    dataset = models.Dataset.query.get(dataset_id)
    dataset.species_objs.delete()
    dataset.habitat_objs.delete()
    if dataset.checklist:
        dataset.habitat_checklist.delete()
        dataset.species_checklist.delete()
    models.db.session.commit()
    dataset.checklist_id = None
    models.db.session.delete(dataset)
    models.db.session.commit()
    flask.flash(u"Setul de date a fost șters.", 'success')
    next_url = request.values.get('next', flask.url_for('.home'))
    return flask.redirect(next_url)


@aggregation.route('/raport/<int:dataset_id>')
@require(Permission(need.authenticated))
def report(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)

    def reports(ds):
        ROLE = 'assessment'
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
    return flask.render_template('aggregation/report.html', dataset=dataset)


@aggregation.route('/preview/<int:dataset_id>/')
def post_preview(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)

    return flask.render_template(
        'aggregation/preview/post.html',
        dataset=dataset,
    )


class DashboardView(View):
    methods = ['GET']

    def get_context_data(self):
        dal_object = self.ds_model(self.dataset_id)
        dataset = models.Dataset.query.get_or_404(self.dataset_id)
        object_regions = dal_object.get_subject_region_overview_aggregation()

        relevant_regions = set(reg for n, reg in object_regions)
        bioreg_list = dal.get_biogeo_region_list(relevant_regions)

        if dataset.preview:
            tabmenu = get_tabmenu_preview(dataset)
        else:
            tabmenu = list(get_tabmenu_data(dataset))
        return {
            'current_tab': self.current_tab,
            'bioreg_list': bioreg_list,
            'tabmenu_data': tabmenu,
            'dataset_url': flask.url_for('.dashboard',
                                         dataset_id=self.dataset_id),
            'dataset_id': self.dataset_id,
            'object_list': self.get_object_list(dataset),
            'object_regions': object_regions,
            'dataset': dataset,
            'habitat_count': dataset.habitat_objs.count(),
            'species_count': dataset.species_objs.count(),
        }

    def dispatch_request(self, *args, **kwargs):
        self.dataset_id = kwargs['dataset_id']
        return flask.render_template(
            'aggregation/dashboard.html',
            **self.get_context_data()
        )


class HabitatsDashboard(DashboardView):
    current_tab = 'H'
    ds_model = dal.HabitatDal

    def get_object_list(self, dataset):
        if dataset.preview:
            return set([h.habitat for h in dataset.habitat_objs])
        return dal.get_habitat_list()


aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/',
                         view_func=HabitatsDashboard.as_view('habitats'))


class SpeciesDashboard(DashboardView):
    ds_model = dal.SpeciesDal

    def get_object_list(self, dataset):
        if dataset.preview:
            return set([s.species for s in dataset.species_objs])
        return dal.get_species_list(self.group_code)

    def dispatch_request(self, *args, **kwargs):
        self.group_code = kwargs['group_code']
        self.current_tab = 'S' + self.group_code
        return super(SpeciesDashboard, self).dispatch_request(*args, **kwargs)


aggregation.add_url_rule('/dataset/<int:dataset_id>/species/<group_code>',
                         view_func=SpeciesDashboard.as_view('species'))


@aggregation.route('/dataset/<int:dataset_id>/')
def dashboard(dataset_id):
    dataset = models.Dataset.query.get(dataset_id)
    if dataset.habitat_objs.count():
        return flask.redirect(flask.url_for('.habitats',
                                            dataset_id=dataset_id))
    species = dataset.species_objs.first()
    if species:
        return flask.redirect(flask.url_for(
            '.species',
            dataset_id=dataset_id,
            group_code=species.species.lu.group_code,
        ))
    return flask.redirect(flask.url_for('.habitats',
                                        dataset_id=dataset_id))


class RecordViewMixin(object):
    template_base = 'aggregation/record.html'
    success_message = u"Înregistrarea a fost actualizată"

    def get_next_url(self):
        if request.form.get('submit', None) == 'finalize':
            return record_finalize_toggle_url(self.record, True)
        return record_edit_url(self.record)

    def setup_record_and_form(self, record_id=None, comment_id=None):
        if record_id:
            self.new_record = False
            self.record = self.record_cls.query.get_or_404(record_id)
            perm_edit_record(self.record).test()
            self.object = self.record
            if self.object.cons_role == 'assessment':
                self.object.cons_role = 'final-draft'
            self.original_data = self.parse_commentform(self.object)
            if request.method == 'POST':
                form_data = request.form
            else:
                form_data = MultiDict(flatten_dict(self.original_data))
            self.form = self.form_cls(form_data)

        else:
            raise RuntimeError("Need at least one of "
                               "record_id and comment_id")


class HabitatRecordView(RecordViewMixin, HabitatCommentView):
    template = 'aggregation/record-habitat.html'
    missing_template = 'aggregation/record-habitat-missing.html'
    comment_history_view = 'history_aggregation.habitat_comments'

    def setup_template_context(self):
        self.dataset = get_habitat_dal(self.dataset_id)
        super(HabitatRecordView, self).setup_template_context()
        self.template_ctx.update(**{
            'dataset_id': self.dataset_id
        })

    def get_dashboard_url(self, subject):
        if flask.current_app.testing:
            return request.url

        return flask.url_for('.habitats', dataset_id=self.dataset_id)


aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>/',
                         view_func=HabitatRecordView.as_view('habitat-edit'))


class SpeciesRecordView(RecordViewMixin, SpeciesCommentView):
    template = 'aggregation/record-species.html'
    missing_template = 'aggregation/record-species-missing.html'
    comment_history_view = 'history_aggregation.species_comments'

    def setup_template_context(self):
        self.dataset = get_species_dal(self.dataset_id)
        super(SpeciesRecordView, self).setup_template_context()
        self.template_ctx.update(**{
            'dataset_id': self.dataset_id,
            'group_code': self.record.species.lu.group_code,
            'app_name': 'aggregation',
        })

    def get_dashboard_url(self, subject):
        if flask.current_app.testing:
            return request.url

        return flask.url_for('.species',
                             dataset_id=self.dataset_id,
                             group_code=self.record.species.lu.group_code)


aggregation.add_url_rule('/dataset/<int:dataset_id>/specii/<int:record_id>/',
                         view_func=SpeciesRecordView.as_view('species-edit'))


class IndexViewMixin(object):
    def dispatch_request(self, dataset_id, record_id):
        self.dataset_id = dataset_id
        self.record = self.model_cls.query.get_or_404(record_id)
        region = dal.get_biogeo_region(self.record.region)
        context = self.get_template_context()
        context.update(**{
            'dataset_id': self.dataset_id,
            'assessment': self.parse_record(self.record),
            'record': self.record,
            'region': region,
            'topic_template': self.topic_template,
        })
        return flask.render_template(self.template_name, **context)


class HabitatIndexView(IndexViewMixin, View):
    topic_template = 'habitat/topic.html'
    template_name = 'aggregation/index-habitat.html'
    model_cls = models.DataHabitattypeRegion
    parse_record = staticmethod(schemas.parse_habitat)

    def get_template_context(self):
        return {
            'type': 'habitat',
        }


aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>/'
                         'index/',
                         view_func=HabitatIndexView.as_view('habitat-index'))

aggregation.route('/habitate/detalii/<int:record_id>',
                  endpoint='detail-habitat')(detail_habitat)


class SpeciesIndexView(IndexViewMixin, View):
    topic_template = 'species/topic.html'
    template_name = 'aggregation/index-species.html'
    model_cls = models.DataSpeciesRegion
    parse_record = staticmethod(schemas.parse_species)

    def get_template_context(self):
        return {
            'group_code': self.record.species.lu.group_code,
            'type': 'species',
        }


aggregation.add_url_rule('/dataset/<int:dataset_id>/specii/<int:record_id>/'
                         'index/',
                         view_func=SpeciesIndexView.as_view('species-index'))

aggregation.route('/specii/detalii/<int:record_id>',
                  endpoint='detail-species')(detail_species)


class RecordDetails(View):
    template_base = 'aggregation/record-details.html'

    def dispatch_request(self, dataset_id, record_id):
        self.record = self.record_cls.query.get(record_id)
        context = self.get_context_data()
        context.update({
            'record': self.record_parser(self.record),
            'record_obj': self.record,
            'region': dal.get_biogeo_region(self.record.region),
            'subject': self.record.subject,
            'dataset_id': dataset_id,
            'pressures': self.record.get_pressures().all(),
            'threats': self.record.get_threats().all(),
            'measures': self.record.measures.all(),
            'template_base': self.template_base,
            'comment_history_view': self.comment_history_view,
            'finalized': self.record.is_final(),
        })
        return flask.render_template(self.template_name, **context)


class SpeciesDetails(RecordDetails):
    record_cls = models.DataSpeciesRegion
    template_name = 'species/detail.html'
    record_parser = staticmethod(schemas.parse_species)
    comment_history_view = 'history_aggregation.species_comments'

    def get_context_data(self):
        return {'group_code': self.record.species.lu.group_code}


class HabitatDetails(RecordDetails):
    record_cls = models.DataHabitattypeRegion
    template_name = 'habitat/detail.html'
    record_parser = staticmethod(schemas.parse_habitat)
    comment_history_view = 'history_aggregation.habitat_comments'

    def get_context_data(self):
        return {'species': self.record.species.all()}


aggregation.add_url_rule('/dataset/<int:dataset_id>/specii/<int:record_id>'
                         '/details',
                         view_func=SpeciesDetails.as_view('species-details'))

aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>'
                         '/details',
                         view_func=HabitatDetails.as_view('habitat-details'))


class RecordFinalToggle(View):
    def __init__(self, finalize=True):
        self.finalize = finalize

    def dispatch_request(self, dataset_id, record_id):
        self.record = self.record_cls.query.get(record_id)
        if self.finalize:
            perm_finalize_record(self.record).test()
            data = self.parse_commentform(self.record)
            form = self.form_cls(MultiDict(flatten_dict(data)))
            if not form.final_validate():
                flask.flash(u"Înregistrarea NU e completă", 'danger')
                return flask.redirect(record_edit_url(self.record))
            if self.record.cons_role == 'final-draft':
                self.record.cons_status = FINALIZED_STATUS
            elif self.record.cons_role == 'assessment':
                self.record.cons_status = 'unmodified'
            self.record.cons_role = 'final'
            flask.flash(u"Înregistrarea a fost finalizată.", 'success')
        else:
            perm_definalize_record(self.record).test()
            if self.record.cons_status == 'unmodified':
                self.record.cons_role = 'assessment'
            else:
                self.record.cons_role = 'final-draft'
            self.record.cons_status = NEW_STATUS
            flask.flash(u"Înregistrarea a fost readusă în lucru.", 'warning')
        models.db.session.add(self.record)
        models.db.session.commit()
        if self.finalize:
            return flask.redirect(record_details_url(self.record))
        else:
            return flask.redirect(record_edit_url(self.record))


class SpeciesFinalToggle(RecordFinalToggle):
    record_cls = models.DataSpeciesRegion
    form_cls = forms.SpeciesComment
    parse_commentform = staticmethod(schemas.parse_species_commentform)


class HabitatFinalToggle(RecordFinalToggle):
    record_cls = models.DataHabitattypeRegion
    form_cls = forms.HabitatComment
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)


aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>'
                         '/finalize',
                         view_func=HabitatFinalToggle.as_view(
                             'habitat-finalize',
                             finalize=True))

aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>'
                         '/definalize',
                         view_func=HabitatFinalToggle.as_view(
                             'habitat-definalize',
                             finalize=False))

aggregation.add_url_rule('/dataset/<int:dataset_id>/specii/<int:record_id>'
                         '/finalize',
                         view_func=SpeciesFinalToggle.as_view(
                             'species-finalize',
                             finalize=True))

aggregation.add_url_rule('/dataset/<int:dataset_id>/specii/<int:record_id>'
                         '/definalize',
                         view_func=SpeciesFinalToggle.as_view(
                             'species-definalize',
                             finalize=False))


@aggregation.route('/refvals/<page>')
def refvals(page):
    subject = request.args.get('subject')
    if page == 'species':
        refvals = load_species_refval()
    elif page == 'habitat':
        refvals = load_habitat_refval()
    else:
        flask.abort(404)

    data = [(k[len(subject)+1:], v) for k, v in refvals.iteritems() if k.startswith(subject)]
    return flask.render_template('aggregation/preview/refvals.html',
                                 refvalues=data)
