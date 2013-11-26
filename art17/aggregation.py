from datetime import datetime
import flask
import flask.views
from werkzeug.datastructures import MultiDict
from art17 import models, dal
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


def record_edit_url(subject, region, dataset_id):
    if isinstance(subject, models.DataHabitat):
        habitat = models.DataHabitattypeRegion.query.filter_by(
            cons_dataset_id=dataset_id,
            habitat=subject,
            region=region.code,
        ).first()
        if habitat:
            return flask.url_for('.habitat',
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
            return flask.url_for('.species-edit',
                                 dataset_id=dataset_id,
                                 record_id=species.id,
            )
    return '#TODO'


@aggregation.app_context_processor
def inject_funcs():
    return dict(home_url=flask.url_for('aggregation.home'),
                record_edit_url=record_edit_url,
    )


@aggregation.route('/')
def home():
    dataset_list = models.Dataset.query.order_by(models.Dataset.date).all()
    return flask.render_template('aggregation/home.html', **{
        'dataset_list': dataset_list,
    })


@aggregation.route('/agregare', methods=['GET', 'POST'])
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


@aggregation.route('/dataset/<int:dataset_id>')
def dataset(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)
    return flask.render_template('aggregation/dataset.html', **{
        'dataset': dataset,
        'habitat_count': dataset.habitat_objs.count(),
        'species_count': dataset.species_objs.count(),
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
        dataset = self.ds_model(self.dataset_id)
        return {
            'current_tab': self.current_tab,
            'bioreg_list': dal.get_biogeo_region_list(),
            'tabmenu_data': list(get_tabmenu_data(self.dataset_id)),
            'dataset_url': flask.url_for('.dataset', dataset_id=self.dataset_id),
            'dataset_id': self.dataset_id,
            'object_list': self.get_object_list(),
            'object_regions': dataset.get_subject_region_overview(),
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


class HabitatRecordView(HabitatCommentView, RecordViewMixin):

    template = 'aggregation/record-habitat.html'
    template_base = 'aggregation/record.html'

    def get_next_url(self):
        return flask.url_for('.habitats', dataset_id=self.dataset_id)

    def setup_template_context(self):
        super(HabitatRecordView, self).setup_template_context()
        self.template_ctx.update(**{
            'dataset_id': self.dataset_id
        })


aggregation.add_url_rule('/dataset/<int:dataset_id>/habitate/<int:record_id>/',
                         view_func=HabitatRecordView.as_view('habitat'))


class SpeciesRecordView(SpeciesCommentView, RecordViewMixin):

    template = 'aggregation/record-species.html'
    template_base = 'aggregation/record.html'

    def get_next_url(self):
        return flask.url_for('.species', dataset_id=self.record.cons_dataset_id,
                             group_code=self.record.species.lu.group_code)

    def setup_template_context(self):
        super(SpeciesRecordView, self).setup_template_context()
        self.template_ctx.update(**{
            'dataset_id': self.dataset_id,
            'group_code': self.record.species.lu.group_code,
        })


aggregation.add_url_rule('/dataset/<int:dataset_id>/specii/<int:record_id>/',
                         view_func=SpeciesRecordView.as_view('species-edit'))
