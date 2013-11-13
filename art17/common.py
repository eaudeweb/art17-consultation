# encoding: utf-8

import re
from datetime import datetime
from dateutil import tz
from decimal import Decimal
import urllib
import logging
from babel.dates import format_datetime
from jinja2 import evalcontextfilter, Markup, escape
import flask
import flask.views
from flask.ext.principal import Permission, Denial
from flask.ext.script import Manager
from werkzeug.datastructures import MultiDict
from sqlalchemy import func
from art17 import models
from art17.auth import need
import lookup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATE_FORMAT = {
    'day': u'd\u00a0MMM',
    'long': u'd\u00a0MMMM\u00a0y\u00a0HH:mm',
}

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

STATUS_OPTIONS = [
    ('new',         u"-- neevaluat"),
    ('investigate', u"!! necesită mai multe investigații"),
    ('incomplete',  u"CO necesită completări/corecții"),
    ('approved',    u"OK propus pentru păstrare"),
    ('rejected',    u"REJ refuzat, motive în replică"),
    ('invalid',     u"NO invalid"),
    ('question',    u"?? discutabil"),
]

EDITABLE_STATUS_LIST = ['new', 'investigate', 'incomplete', 'question']

STATUS_VALUES = list(dict(STATUS_OPTIONS))

APPROVED_STATUS = 'approved'
assert APPROVED_STATUS in STATUS_VALUES

CONCLUSION_COLOR = {
    'FV': '71A057',
    'U1': 'E7E737',
    'U2': 'F76C27',
    'XX': 'FFFFFF',
}


def perm_create_comment(record):
    return Permission(need.authenticated)


def perm_edit_comment(comment):
    if comment.cons_status not in EDITABLE_STATUS_LIST:
        return Permission(need.impossible)

    if comment.cons_user_id:
        return Permission(need.admin, need.user_id(comment.cons_user_id))

    else:
        return Permission(need.admin)


def perm_update_comment_status(comment):
    return Permission(need.admin)


def perm_delete_comment(comment):
    if comment.cons_status not in EDITABLE_STATUS_LIST:
        return Permission(need.impossible)

    if comment.cons_status == APPROVED_STATUS:
        return Denial(need.everybody)

    elif comment.cons_user_id:
        return Permission(need.admin, need.user_id(comment.cons_user_id))

    else:
        return Permission(need.admin)


common = flask.Blueprint('common', __name__)


@common.app_context_processor
def inject_permissions():
    return {
        'perm_create_comment': perm_create_comment,
        'perm_edit_comment': perm_edit_comment,
        'perm_update_comment_status': perm_update_comment_status,
        'perm_delete_comment': perm_delete_comment,
    }


@common.app_context_processor
def inject_constants():
    return {
        'TREND_NAME': lookup.TREND_NAME,
        'METHODS_USED': lookup.METHODS_USED,
        'LU_FV_RANGE_OP': lookup.LU_FV_RANGE_OP,
        'LU_FV_RANGE_OP_FUNCT': lookup.LU_FV_RANGE_OP_FUNCT,
        'LU_POP_NUMBER': lookup.LU_POP_NUMBER,
        'CONCLUSIONS': lookup.CONCLUSIONS,
        'LU_REASONS_FOR_CHANGE': lookup.LU_REASONS_FOR_CHANGE,
        'QUALITY': lookup.QUALITY,
        'STATUS_OPTIONS': STATUS_OPTIONS,
        'METHODS_PRESSURES': lookup.METHODS_PRESSURES,
        'METHODS_THREATS': lookup.METHODS_THREATS,
        'GENERALSTATUS_CHOICES': dict(models.db.session.query(
                                    models.LuPresence.code,
                                    models.LuPresence.name).all())
    }


@common.app_template_filter('local_date')
def local_date(value, format='day'):
    if not value:
        return ''
    utc = tz.gettz('UTC')
    local_tz = tz.gettz('Europe/Bucharest')
    local_value = value.replace(tzinfo=utc).astimezone(local_tz)
    return format_datetime(local_value, DATE_FORMAT[format], locale='ro')


@common.app_template_filter('nl2br')
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def flatten_dict(data):
    rv = {}
    for k, v in data.items():
        if isinstance(v, dict):
            for kx, vx in flatten_dict(v).items():
                rv[k + '.' + kx] = vx
        else:
            rv[k] = '' if v is None else unicode(v)
    return rv


def json_encode_more(value):
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, datetime):
        return value.isoformat()

    raise TypeError


class IndexView(flask.views.View):

    def parse_request(self):
        self.subject_code = flask.request.args.get(self.subject_name)

        if self.subject_code:
            self.subject = (
                self.subject_cls.query
                    .filter_by(code=self.subject_code)
                    .join(models.DataSpecies.lu)
                    .first_or_404()
            )
        else:
            self.subject = None

        self.region_code = flask.request.args.get('region', '')
        if self.region_code:
            self.region = (
                models.LuBiogeoreg.query
                    .filter_by(code=self.region_code)
                    .first_or_404()
            )
        else:
            self.region = None

        if self.subject:
            self.topic_list = self.get_topics(self.subject, self.region)

            CommentReply = models.CommentReply
            reply_query = (
                models.db.session
                .query(CommentReply.parent_id, func.count(CommentReply.id))
                .filter(CommentReply.parent_table == self.blueprint)
                .group_by(CommentReply.parent_id)
            )
            self.reply_counts = dict(reply_query)

        self.subject_list = (
            self.subject_cls.query
                .join(self.record_cls)
                .order_by(self.subject_cls.code)
        )

    def get_topics(self, subject, region):
        region_data_map = {}
        for record in self.get_records(subject, region):
            if record.region not in region_data_map:
                region_data_map[record.region] = {
                    'region': record.lu,
                    'comments': [],
                }

            region_data = region_data_map[record.region]

            if record.cons_role == 'assessment':
                region_data['assessment'] = self.parse_record(record)

            else:
                if not record.cons_deleted:
                    r = self.parse_record(record, is_comment=True)
                    region_data['comments'].append(r)

        return list(region_data_map.values())

    def get_pressures(self, record):
        return record.pressures.all()

    def get_measures(self, record):
        return record.measures.all()

    def prepare_context(self):
        self.ctx.update({
            'topic_template': self.topic_template,
            'subject_list': self.get_subject_list(),
            'current_subject_code': self.subject_code,
            'current_region_code': self.region_code,
            'comment_next': self.get_comment_next_url(),
            'blueprint': self.blueprint,
        })

        if self.subject:
            map_colors = [{
                    'region': t['region'].code,
                    'code': CONCLUSION_COLOR.get(
                        t['assessment']['overall_assessment']['value']),
                } for t in self.topic_list]
            self.ctx.update({
                'code': self.subject.code,
                'name': self.subject.lu.display_name,
                'topic_list': self.topic_list,
                'reply_counts': self.reply_counts,
                'map_url': self.map_url_template.format(**{
                    self.subject_name: self.subject.code,
                    'regions': urllib.quote(flask.json.dumps(map_colors)),
                }),
            })

    def dispatch_request(self):
        self.parse_request()
        self.ctx = {}
        self.prepare_context()
        return flask.render_template(self.template, **self.ctx)


class CommentView(flask.views.View):

    methods = ['GET', 'POST']

    def dispatch_request(self, record_id=None, comment_id=None):
        if record_id:
            new_comment = True
            self.record = self.record_cls.query.get_or_404(record_id)
            perm_create_comment(self.record).test()
            self.comment = self.comment_cls(
                cons_role='comment',
                cons_user_id=flask.g.identity.id,
                cons_date=datetime.utcnow(),
            )
            form = self.form_cls(flask.request.form)

        elif comment_id:
            new_comment = False
            self.comment = (self.comment_cls
                                    .query.get_or_404(comment_id))
            perm_edit_comment(self.comment).test()
            self.record = self.record_for_comment(self.comment)
            old_data = self.parse_commentform(self.comment)
            if flask.request.method == 'POST':
                form_data = flask.request.form
            else:
                form_data = MultiDict(flatten_dict(old_data))
            form = self.form_cls(form_data)

        else:
            raise RuntimeError("Need at least one of "
                               "record_id and comment_id")

        self.setup_template_context()
        self.template_ctx['next_url'] = flask.request.args.get('next')

        if flask.request.method == 'POST' and form.validate():
            self.link_comment_to_record()

            self.flatten_commentform(form.data, self.comment)
            models.db.session.add(self.comment)

            app = flask.current_app._get_current_object()
            if new_comment:
                self.add_signal.send(app, ob=self.comment,
                                          new_data=form.data)
            else:
                self.edit_signal.send(app, ob=self.comment,
                                      old_data=old_data, new_data=form.data)

            models.db.session.commit()

            return flask.render_template(self.template_saved,
                                         **self.template_ctx)

        self.template_ctx['form'] = form
        return flask.render_template(self.template, **self.template_ctx)


class CommentStateView(flask.views.View):

    methods = ['POST']

    def dispatch_request(self, comment_id):
        comment = self.comment_cls.query.get_or_404(comment_id)
        next_url = flask.request.form['next']
        new_status = flask.request.form['status']
        if new_status not in STATUS_VALUES:
            flask.abort(403)
        old_status = comment.cons_status
        comment.cons_status = new_status
        app = flask.current_app._get_current_object()
        self.signal.send(app, ob=comment,
                         old_data=old_status, new_data=new_status)
        models.db.session.commit()
        return flask.redirect(next_url)


class CommentDeleteView(flask.views.View):

    methods = ['POST']

    def dispatch_request(self, comment_id):
        comment = self.comment_cls.query.get_or_404(comment_id)
        perm_delete_comment(comment).test()
        next_url = flask.request.form['next']
        comment.cons_deleted = True
        app = flask.current_app._get_current_object()
        old_data = self.parse_commentform(comment)
        old_data['_status'] = comment.cons_status
        self.signal.send(app, ob=comment, old_data=old_data)
        models.db.session.commit()
        return flask.redirect(next_url)


cons_manager = Manager()
