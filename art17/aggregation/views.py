# encoding: utf-8

from datetime import datetime
import flask
from flask import request
from flask.views import View
from werkzeug.datastructures import MultiDict
from wtforms import Form, SelectField

from art17 import models, forms, schemas, dal
from art17.aggregation import (
    aggregation,
    check_aggregation_perm,
    create_aggregation,
    create_preview_aggregation,
    get_tabmenu_data,
    get_tabmenu_preview,
    perm_edit_record,
    perm_finalize_record,
    perm_definalize_record,
    get_habitat_checklist,
    get_species_checklist,
    check_aggregation_preview_perm)
from art17.aggregation.utils import (
    record_edit_url,
    record_details_url,
    record_finalize_toggle_url,
)
from art17.auth import admin_permission
from art17.common import (
    flatten_dict,
    flatten_errors,
    FINALIZED_STATUS,
    NEW_STATUS,
)
from art17.habitat import detail as detail_habitat, HabitatCommentView
from art17.lookup import CONCLUSIONS
from art17.species import detail as detail_species, SpeciesCommentView


class PreviewForm(Form):
    subject = SelectField(default='')


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
    dataset_list = (
        models.Dataset.query
        .filter_by(preview=None)
        .order_by(models.Dataset.date)
        .all()
    )
    preview_list = (
        models.Dataset.query
        .filter_by(preview=True, checklist=None, user_id=flask.g.identity.id)
        .order_by(models.Dataset.date)
        .all()
    )
    return flask.render_template('aggregation/home.html', **{
        'dataset_list': dataset_list,
        'preview_datasets': preview_list,
    })


@aggregation.route('/executa_agregare', methods=['GET', 'POST'])
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
    check_aggregation_preview_perm()
    if page == 'habitat':
        qs = get_habitat_checklist(distinct=True)
    elif page == 'species':
        qs = get_species_checklist(distinct=True)
    else:
        raise NotImplementedError()
    qs = list(qs)
    report = None
    dataset = None
    form = PreviewForm(request.form)
    form.subject.choices = qs
    qs_dict = dict(qs)
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
        else:
            flask.flash('Invalid form', 'error')
    return flask.render_template('aggregation/preview.html', **{
        'form': form,
        'dataset': dataset,
        'report': report,
    })


@aggregation.route('/sterge/<int:dataset_id>', methods=['POST'])
@admin_permission.require()
def delete_dataset(dataset_id):
    dataset = models.Dataset.query.get(dataset_id)
    dataset.species_objs.delete()
    dataset.habitat_objs.delete()
    models.db.session.delete(dataset)
    models.db.session.commit()
    flask.flash(u"Setul de date a fost șters.", 'success')
    next_url = request.values.get('next', flask.url_for('.home'))
    return flask.redirect(next_url)


@aggregation.route('/raport/<int:dataset_id>')
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
        return data

    dataset.reports = reports(dataset)
    return flask.render_template('aggregation/report.html', dataset=dataset)


class DashboardView(View):

    methods = ['GET']

    def get_context_data(self):
        dal_object = self.ds_model(self.dataset_id)
        self.dataset = models.Dataset.query.get_or_404(self.dataset_id)
        object_regions = dal_object.get_subject_region_overview_aggregation()
        #bioreg_list = dal.get_biogeo_region_list()

        relevant_regions = set(reg for n, reg in object_regions)
        bioreg_list = [
            r for r in dal.get_biogeo_region_list()
            if r.code in relevant_regions
        ]

        if self.dataset.preview:
            tabmenu = get_tabmenu_preview(self.dataset)
        else:
            tabmenu = list(get_tabmenu_data(self.dataset))
        return {
            'current_tab': self.current_tab,
            'bioreg_list': bioreg_list,
            'tabmenu_data': tabmenu,
            'dataset_url': flask.url_for('.dashboard',
                                         dataset_id=self.dataset_id),
            'dataset_id': self.dataset_id,
            'object_list': self.get_object_list(),
            'object_regions': object_regions,
            'dataset': self.dataset,
            'habitat_count': self.dataset.habitat_objs.count(),
            'species_count': self.dataset.species_objs.count(),
        }

    def dispatch_request(self, *args, **kwargs):
        self.dataset_id = kwargs['dataset_id']
        return flask.render_template(
            'aggregation/dashboard.html',
            **self.get_context_data()
        )


class HabitatsDashboard(DashboardView):

    current_tab = 'H'
    ds_model = dal.HabitatDataset

    def get_object_list(self):
        if self.dataset.preview:
            return set([h.habitat for h in self.dataset.habitat_objs])
        return dal.get_habitat_list()

aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/',
                         view_func=HabitatsDashboard.as_view('habitats'))


class SpeciesDashboard(DashboardView):

    ds_model = dal.SpeciesDataset

    def get_object_list(self):
        if self.dataset.preview:
            return set([s.species for s in self.dataset.species_objs])
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
    comment_history_view = 'history_aggregation.habitat_comments'

    def setup_template_context(self):
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
    comment_history_view = 'history_aggregation.species_comments'

    def setup_template_context(self):
        super(SpeciesRecordView, self).setup_template_context()
        self.template_ctx.update(**{
            'dataset_id': self.dataset_id,
            'group_code': self.record.species.lu.group_code,
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
            'finalized': self.record.cons_role == 'final',
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
                errors = flatten_errors(form.errors)
                flask.flash(u"Înregistrarea NU a fost finalizată, deoarece este"
                            u" incompletă. Probleme:\n%s" % errors, 'danger')
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
