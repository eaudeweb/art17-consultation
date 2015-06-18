# encoding: utf-8
import flask
from flask import current_app
from flask.ext.principal import Permission

from art17 import models
from art17 import auth
from art17.common import get_year_start, get_year_end

CONFIGURATION = {
    'CONSULTATION': {
        'SPECIES_MAP_URL': u"URL serviciu de hărți pentru specii",
        'HABITAT_MAP_URL': u"URL serviciu de hărți pentru habitate",
        'CONSULTATION_DATASET': u"Setul de date în consultare",
        'SPECIES_PRIMARY_DATA_URL': u"URL serviciu de date primare pentru specii",
        'HABITAT_PRIMARY_DATA_URL': u"URL serviciu de date primare pentru habitate",
    },
    'AGGREGATION': {
        'REPORTING_ID': u"Lista de verificare curentă",
    },
}

CONFIG_TEMPLATES = {
    'CONSULTATION': 'consultation/config.html',
    'AGGREGATION': 'aggregation/config.html',
}

config = flask.Blueprint('config', __name__)


@config.route('/config', methods=['GET', 'POST'])
@auth.require(Permission(auth.need.admin, auth.need.reporter))
def form():
    config_key = current_app.config.get('CONFIG_SET', 'CONSULTATION')
    if config_key not in CONFIGURATION:
        raise ValueError('Invalid config key')

    config_set = CONFIGURATION[config_key]
    template_name = CONFIG_TEMPLATES[config_key]
    config_rows = models.Config.query.filter(
        models.Config.id.in_(config_set.keys())
    )
    if flask.request.method == 'POST':
        for row in config_rows:
            row.value = flask.request.form[row.id]
        models.db.session.commit()
        flask.flash(u"Configurația a fost salvată.", 'success')
        return flask.redirect(flask.url_for('.form'))

    context = {
        'CONFIG_LABEL': config_set,
        'config_rows': config_rows,
        'page': 'config',
    }

    if config_key == 'AGGREGATION':
        year_start = get_year_start()
        year_end = get_year_end(year_start)
        context.update({
            'year_start': year_start,
            'year_end': year_end,
            'base_template': 'aggregation/admin.html',
        })
    else:
        context['base_template'] = ''

    return flask.render_template(template_name, **context)


@config.route('/config/period', methods=['GET', 'POST'])
@auth.require(Permission(auth.need.admin, auth.need.reporter))
def new_period():
    reporting_begin = models.Config.query.get('REPORTING_BEGIN')
    year_start = get_year_start() + current_app.config['REPORTING_FREQUENCY']
    year_end = get_year_end(year_start)

    if flask.request.method == 'POST':
        reporting_begin.value = str(year_start)
        models.db.session.commit()
        flask.flash(u"Configurația a fost salvată.", 'success')
        return flask.redirect(flask.url_for('.form'))

    context = {
        'year_start': year_start,
        'year_end': year_end,
        'base_template': 'aggregation/admin.html',
        'page': 'config',
    }
    return flask.render_template('aggregation/admin/new_period.html', **context)


def get_config_value(name, default=''):
    row = models.Config.query.filter_by(id=name).first()
    if row and row.value:
        return row.value
    else:
        return default
