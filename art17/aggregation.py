# encoding: utf-8

from datetime import datetime
from blinker import Signal
import flask
import flask.views
from werkzeug.datastructures import MultiDict
from art17 import models, dal, schemas
from art17.common import flatten_dict, perm_edit_record
from art17.habitat import HabitatCommentView
from art17.species import SpeciesCommentView

aggregation = flask.Blueprint('aggregation', __name__)


def get_tabmenu_data(dataset_id):
    yield {
        'url': flask.url_for('.habitats', dataset_id=dataset_id),
        'label': "Habitate",
        'code': 'H',
    }
    for group in dal.get_species_groups():
        yield {
            'url': flask.url_for('.species',
                                 group_code=group.code,
                                 dataset_id=dataset_id),
            'label': group.description,
            'code': 'S' + group.code,
        }


def record_index_url(subject, region, dataset_id):
    if isinstance(subject, models.DataHabitat):
        habitat = models.DataHabitattypeRegion.query.filter_by(
            cons_dataset_id=dataset_id,
            habitat=subject,
            region=region.code,
        ).first()
        if habitat:
            return flask.url_for('.habitat-index',
                                 dataset_id=dataset_id,
                                 record_id=habitat.id,
            )
    if isinstance(subject, models.DataSpecies):
        species = models.DataSpeciesRegion.query.filter_by(
            cons_dataset_id=dataset_id,
            species=subject,
            region=region.code,
        ).first()
        if species:
            return flask.url_for('.species-index',
                                 dataset_id=dataset_id,
                                 record_id=species.id,
            )
    raise RuntimeError("Expecting a speciesregion or a habitattyperegion")


def record_dashboard_url(record):
    if isinstance(record, models.DataHabitattypeRegion):
        return flask.url_for('.habitats', dataset_id=record.cons_dataset_id)
    elif isinstance(record, models.DataSpeciesRegion):
        return flask.url_for('.species',
                             dataset_id=record.cons_dataset_id,
                             group_code=record.subject.lu.group_code)
    raise RuntimeError("Expecting a species or a habitat object")


@aggregation.app_context_processor
def inject_funcs():
    return dict(home_url=flask.url_for('aggregation.home'),
                record_index_url=record_index_url,
                record_dashboard_url=record_dashboard_url,
    )


@aggregation.route('/')
def home():
    dataset_list = models.Dataset.query.order_by(models.Dataset.date).all()
    return flask.render_template('aggregation/home.html', **{
        'dataset_list': dataset_list,
    })


@aggregation.route('/executa_agregare', methods=['GET', 'POST'])
def aggregate():
    if flask.request.method == 'POST':
        q = "SELECT SYS_CONTEXT('USERENV', 'SESSION_USER') FROM DUAL"
        result = execute_on_primary(q).scalar()
        dataset = create_aggregation(datetime.utcnow(), flask.g.identity.id)
        models.db.session.commit()

    else:
        result = None
        dataset = None

    return flask.render_template('aggregation/aggregate.html', **{
        'result': result,
        'dataset': dataset,
    })


def execute_on_primary(query):
    app = flask.current_app
    aggregation_engine = models.db.get_engine(app, 'primary')
    return models.db.session.execute(query, bind=aggregation_engine)


def create_aggregation(timestamp, user_id):
    dataset = models.Dataset(
        date=timestamp,
        user_id=user_id,
    )
    models.db.session.add(dataset)

    habitat_row = models.DataHabitattypeRegion(
        dataset=dataset,
        habitat=models.DataHabitat.query.filter_by(code='8230').first(),
        region='MBLS',
        cons_role='assessment',
        cons_date=timestamp,
        cons_user_id=user_id,
    )

    species_row = models.DataSpeciesRegion(
        dataset=dataset,
        species=models.DataSpecies.query.filter_by(code='1353').first(),
        region='MBLS',
        cons_role='assessment',
        cons_date=timestamp,
        cons_user_id=user_id,
    )

    return dataset


class DashboardView(flask.views.View):

    methods = ['GET']

    def get_context_data(self):
        dal_object = self.ds_model(self.dataset_id)
        dataset = models.Dataset.query.get_or_404(self.dataset_id)
        return {
            'current_tab': self.current_tab,
            'bioreg_list': dal.get_biogeo_region_list(),
            'tabmenu_data': list(get_tabmenu_data(self.dataset_id)),
            'dataset_url': flask.url_for('.dashboard', dataset_id=self.dataset_id),
            'dataset_id': self.dataset_id,
            'object_list': self.get_object_list(),
            'object_regions': dal_object.get_subject_region_overview(),
            'dataset': dataset,
            'habitat_count': dataset.habitat_objs.count(),
            'species_count': dataset.species_objs.count(),
        }

    def dispatch_request(self, *args, **kwargs):
        self.dataset_id = kwargs['dataset_id']
        return flask.render_template('aggregation/dashboard.html',
                                     **self.get_context_data()
        )


class HabitatsDashboard(DashboardView):

    current_tab = 'H'
    ds_model = dal.HabitatDataset

    def get_object_list(self):
        return dal.get_habitat_list()

aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/',
                         view_func=HabitatsDashboard.as_view('habitats'))


@aggregation.route('/dataset/<int:dataset_id>/')
def dashboard(dataset_id):
    return flask.redirect(flask.url_for('.habitats', dataset_id=dataset_id))


class SpeciesDashboard(DashboardView):

    ds_model = dal.SpeciesDataset

    def get_object_list(self):
        return dal.get_species_list(self.group_code)

    def dispatch_request(self, *args, **kwargs):
        self.group_code = kwargs['group_code']
        self.current_tab = 'S' + self.group_code
        return super(SpeciesDashboard, self).dispatch_request(*args, **kwargs)

aggregation.add_url_rule('/dataset/<int:dataset_id>/species/<group_code>',
                         view_func=SpeciesDashboard.as_view('species'))


class RecordViewMixin(object):

    template_base = 'aggregation/record.html'
    template_saved = 'aggregation/record-saved.html'

    def setup_record_and_form(self, record_id=None, comment_id=None):
        if record_id:
            self.new_record = False
            self.record = self.record_cls.query.get_or_404(record_id)
            perm_edit_record(self.record).test()
            self.object = self.record
            self.original_data = self.parse_commentform(self.object)
            if flask.request.method == 'POST':
                form_data = flask.request.form
            else:
                form_data = MultiDict(flatten_dict(self.original_data))
            self.form = self.form_cls(form_data)

        else:
            raise RuntimeError("Need at least one of "
                               "record_id and comment_id")


class HabitatRecordView(RecordViewMixin, HabitatCommentView):

    template = 'aggregation/record-habitat.html'
    add_signal = Signal()
    edit_signal = Signal()
    success_message = u"Înregistrarea a fost actualizată"

    def get_next_url(self):
        return flask.url_for('.habitat-index', dataset_id=self.dataset_id,
                             record_id=self.record.id)

    def setup_template_context(self):
        super(HabitatRecordView, self).setup_template_context()
        self.template_ctx.update(**{
            'dataset_id': self.dataset_id
        })


aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>/',
                         view_func=HabitatRecordView.as_view('habitat-edit'))


class SpeciesRecordView(RecordViewMixin, SpeciesCommentView):

    template = 'aggregation/record-species.html'
    add_signal = Signal()
    edit_signal = Signal()
    success_message = u"Înregistrarea a fost actualizată"

    def get_next_url(self):
        return flask.url_for('.species-index',
                             dataset_id=self.dataset_id,
                             record_id=self.record.id)

    def setup_template_context(self):
        super(SpeciesRecordView, self).setup_template_context()
        self.template_ctx.update(**{
            'dataset_id': self.dataset_id,
            'group_code': self.record.species.lu.group_code,
        })


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


class HabitatIndexView(IndexViewMixin, flask.views.View):

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

from .habitat import detail as detail_habitat

aggregation.route('/habitate/detalii/<int:record_id>',
                  endpoint='detail-habitat')(detail_habitat)


class SpeciesIndexView(IndexViewMixin, flask.views.View):

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


from .species import detail as detail_species

aggregation.route('/specii/detalii/<int:record_id>',
                  endpoint='detail-species')(detail_species)


class RecordDetails(flask.views.View):

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
        })
        return flask.render_template(self.template_name, **context)


class SpeciesDetails(RecordDetails):

    record_cls = models.DataSpeciesRegion
    template_name = 'species/detail.html'
    record_parser = staticmethod(schemas.parse_species)

    def get_context_data(self):
        return {'group_code': self.record.species.lu.group_code}


class HabitatDetails(RecordDetails):

    record_cls = models.DataHabitattypeRegion
    template_name = 'habitat/detail.html'
    record_parser = staticmethod(schemas.parse_habitat)

    def get_context_data(self):
        return {'species': self.record.species.all()}


aggregation.add_url_rule('/dataset/<int:dataset_id>/specii/<int:record_id>'
                         '/details',
                         view_func=SpeciesDetails.as_view('species-details'))

aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>'
                         '/details',
                         view_func=HabitatDetails.as_view('habitat-details'))
