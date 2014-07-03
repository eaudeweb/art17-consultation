# encoding: utf-8

from datetime import datetime
import flask
from art17 import models, config
from art17 import species
from art17 import habitat
from art17 import replies
from art17.common import json_encode_more, perm_view_history, get_history_object_url
from art17.auth import admin_permission
from art17.dal import get_biogeo_region
from art17.pagination import Paginator

history = flask.Blueprint('history', __name__)
history_consultation = flask.Blueprint('history_consultation', __name__)
history_aggregation = flask.Blueprint('history_aggregation', __name__)


TABLE_LABEL = {
    'data_species_regions': u"evaluare specie",
    'data_habitattype_regions': u"evaluare habitat",
    'comment_replies': u"replică",
}

PER_PAGE = 25


@history.record
def register_handlers(state):
    app = state.app

    connect(species.comment_added, app,
            table='data_species_regions', action='add')
    connect(species.comment_edited, app,
            table='data_species_regions', action='edit')
    connect(species.comment_status_changed, app,
            table='data_species_regions', action='status')
    connect(species.comment_deleted, app,
            table='data_species_regions', action='delete')

    connect(habitat.comment_added, app,
            table='data_habitattype_regions', action='add')
    connect(habitat.comment_edited, app,
            table='data_habitattype_regions', action='edit')
    connect(habitat.comment_status_changed, app,
            table='data_habitattype_regions', action='status')
    connect(habitat.comment_deleted, app,
            table='data_habitattype_regions', action='delete')

    connect(replies.reply_added, app,
            table='comment_replies', action='add')
    connect(replies.reply_removed, app,
            table='comment_replies', action='remove')


def connect(signal, sender, **more_kwargs):
    @signal.connect_via(sender)
    def wrapper(sender, **kwargs):
        kwargs.update(more_kwargs)
        handle_signal(**kwargs)


def handle_signal(table, action, ob, old_data=None, new_data=None, **extra):
    if not ob.id:
        models.db.session.flush()
        assert ob.id
    if table == 'comment_replies':
        record = replies.get_comment_from_reply(ob.parent_table,
                                                ob.parent_id)
        dataset_id = record.cons_dataset_id if record else None
    else:
        dataset_id = ob.cons_dataset_id
    item = models.History(table=table,
                          action=action,
                          object_id=ob.id,
                          dataset_id=dataset_id,
                          date=datetime.utcnow(),
                          user_id=flask.g.identity.id)
    if old_data:
        item.old_data = flask.json.dumps(old_data, default=json_encode_more)
    if new_data:
        item.new_data = flask.json.dumps(new_data, default=json_encode_more)
    models.db.session.add(item)


@history_consultation.context_processor
@history_aggregation.context_processor
def inject_lookup_tables():
    return {
        'TABLE_LABEL': TABLE_LABEL,
    }


@history_consultation.route('/activitate')
@history_aggregation.route('/dataset/<int:dataset_id>/activitate')
@admin_permission.require()
def index(dataset_id=None):
    if dataset_id:
        consultation = False
    else:
        consultation=True
    dataset_id = dataset_id or config.get_config_value('CONSULTATION_DATASET',
                                                       '1')
    page = int(flask.request.args.get('page', 1))
    history_items = models.History.query \
        .filter_by(dataset_id=dataset_id) \
        .order_by(models.History.date.desc()
    )
    count = history_items.count()
    history_items = history_items.paginate(page, PER_PAGE, False).items
    paginator = Paginator(per_page=PER_PAGE, page=page, count=count)

    for item in history_items:
        item.url, item.title = get_history_object_url(item)

    return flask.render_template('history/index.html', **{
        'history_items': history_items,
        'dataset_id': dataset_id,
        'paginator': paginator,
        'consultation': consultation
    })


@history_consultation.route('/activitate/<item_id>')
@history_aggregation.route('/activitate/<item_id>')
@admin_permission.require()
def delta(item_id):
    return flask.render_template('history/delta.html', **{
        'item': models.History.query.get_or_404(item_id),
    })


@history.app_template_filter('pretty_json_data')
def pretty_json_data(json_data):
    data = flask.json.loads(json_data)
    return flask.json.dumps(data, indent=2, sort_keys=True)


@history_consultation.route('/activitate/specii/<subject_code>/<region_code>')
@history_aggregation.route('/dataset/<int:dataset_id>/activitate'
                           '/specii/<subject_code>/<region_code>')
def species_comments(subject_code, region_code, dataset_id=None):
    from art17.species import get_dataset
    dataset = get_dataset(dataset_id)
    items = dataset.get_history(subject_code, region_code)
    subject = dataset.get_subject(subject_code)
    perm_view_history(subject).test()
    return flask.render_template('history/comments.html', **{
        'history_items': items,
        'subject_category': 'specii',
        'subject_code': subject_code,
        'subject': subject,
        'region': get_biogeo_region(region_code),
        'dashboard_url':
            flask.url_for('dashboard.species', group_code=subject.lu.group_code)
            if dataset_id is None else '',
        'record_index_url':
            flask.url_for('species.index', region=region_code,
                          species=subject_code)
            if dataset_id is None else '',
        'region_code': region_code,
    })


@history_consultation.route('/activitate/habitate/<subject_code>/<region_code>')
@history_aggregation.route('/dataset/<int:dataset_id>/activitate'
                           '/habitate/<subject_code>/<region_code>')
def habitat_comments(subject_code, region_code, dataset_id=None):
    from art17.habitat import get_dataset
    dataset = get_dataset(dataset_id)
    items = dataset.get_history(subject_code, region_code)
    subject = dataset.get_subject(subject_code)
    perm_view_history(subject).test()

    return flask.render_template('history/comments.html', **{
        'history_items': items,
        'subject_category': 'habitate',
        'subject_code': subject_code,
        'subject': subject,
        'region': get_biogeo_region(region_code),
        'dashboard_url':
            flask.url_for('dashboard.habitats') if dataset_id is None else '',
        'record_index_url':
            flask.url_for('habitat.index', region=region_code,
                          habitat=subject_code) if dataset_id is None else ''
        ,
        'region_code': region_code,
    })
