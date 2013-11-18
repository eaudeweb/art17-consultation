import flask

aggregation = flask.Blueprint('aggregation', __name__)


@aggregation.app_context_processor
def inject_home_url():
    return dict(home_url=flask.url_for('aggregation.home'))


@aggregation.route('/')
def home():
    return flask.render_template('aggregation/home.html')


@aggregation.route('/agregare')
def aggregate():
    q = "SELECT SYS_CONTEXT('USERENV', 'SESSION_USER') FROM DUAL"
    return flask.render_template('aggregation/aggregate.html', **{
        'result': execute_on_primary(q).scalar(),
    })


def execute_on_primary(query):
    from art17.models import db
    app = flask.current_app
    aggregation_engine = db.get_engine(app, 'primary')
    return db.session.execute(query, bind=aggregation_engine)
