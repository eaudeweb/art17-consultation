from datetime import datetime
import flask
import flask.views
from art17 import models, dal

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


@aggregation.app_context_processor
def inject_home_url():
    return dict(home_url=flask.url_for('aggregation.home'))


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

aggregation.add_url_rule('/dataset/<int:dataset_id>/dashboard/habitate/',
                         view_func=HabitatsDashboard.as_view('habitats'))


class SpeciesDashboard(DashboardView):

    ds_model = dal.SpeciesDataset

    def get_object_list(self):
        return dal.get_species_list(self.group_code)

    def dispatch_request(self, *args, **kwargs):
        self.group_code = kwargs['group_code']
        self.current_tab = 'S' + self.group_code
        return super(SpeciesDashboard, self).dispatch_request(*args, **kwargs)

aggregation.add_url_rule('/dataset/<int:dataset_id>/dashboard/'
                         'species/<group_code>',
                         view_func=SpeciesDashboard.as_view('species'))
