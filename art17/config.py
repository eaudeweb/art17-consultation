# encoding: utf-8
import flask
from art17 import models
from art17 import auth

CONFIG_LABEL = {
    'SPECIES_MAP_URL': u"URL serviciu de hărți pentru specii",
    'HABITAT_MAP_URL': u"URL serviciu de hărți pentru habitate",
    'CONSULTATION_DATASET': u"Setul de date în consultare",
}

config = flask.Blueprint('config', __name__)


@config.route('/config', methods=['GET', 'POST'])
def form():
    auth.admin_permission.test()

    if flask.request.method == 'POST':
        for row in models.Config.query:
            row.value = flask.request.form[row.id]
        models.db.session.commit()
        flask.flash(u"Configurația a fost salvată.", 'success')
        return flask.redirect(flask.url_for('.form'))

    return flask.render_template('config.html', **{
        'CONFIG_LABEL': CONFIG_LABEL,
        'config_rows': models.Config.query.all(),
    })


def get_config_value(name, default=''):
    row = models.Config.query.filter_by(id=name).first()
    if row and row.value:
        return row.value
    else:
        return default
