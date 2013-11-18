import flask

aggregation = flask.Blueprint('aggregation', __name__)


@aggregation.app_context_processor
def inject_home_url():
    return dict(home_url=flask.url_for('aggregation.home'))


@aggregation.route('/')
def home():
    return flask.render_template('aggregation/home.html')
