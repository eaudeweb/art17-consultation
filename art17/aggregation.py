import flask
from art17 import models

aggregation = flask.Blueprint('aggregation', __name__)


@aggregation.app_context_processor
def inject_home_url():
    return dict(home_url=flask.url_for('aggregation.home'))


@aggregation.route('/')
def home():
    return flask.render_template('aggregation/home.html', **{
        'dataset_list': models.Dataset.query.all(),
    })


@aggregation.route('/agregare', methods=['GET', 'POST'])
def aggregate():
    result = None

    if flask.request.method == 'POST':
        q = "SELECT SYS_CONTEXT('USERENV', 'SESSION_USER') FROM DUAL"
        result = execute_on_primary(q).scalar()

    return flask.render_template('aggregation/aggregate.html', **{
        'result': result,
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
