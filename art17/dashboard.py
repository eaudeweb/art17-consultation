import flask


dashboard = flask.Blueprint('dashboard', __name__)


@dashboard.route('/')
def index():
    return flask.render_template('dashboard/index.html')
