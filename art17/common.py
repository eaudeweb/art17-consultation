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
from art17 import dal
from art17.auth import need
from art17 import forms
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


def calculate_identifier_steps(identifier):
    bits = identifier.split(':')
    return [':'.join(bits[:c+1]) for c in range(len(bits))]


def get_roles_for_record(role_base, comment):
    full_name = '%s:%s' % (role_base, comment.identifier)
    steps = calculate_identifier_steps(full_name)
    return [need.role(s) for s in steps]


def perm_create_comment(record):
    return Permission(need.admin, *get_roles_for_record('expert', record))


def perm_edit_comment(comment):
    if comment.cons_status not in EDITABLE_STATUS_LIST:
        return Permission(need.impossible)

    if comment.cons_user_id:
        return Permission(need.admin, need.user_id(comment.cons_user_id))

    else:
        return Permission(need.admin)


def perm_update_comment_status(comment):
    return Permission(need.admin, *get_roles_for_record('reviewer', comment))


def perm_delete_comment(comment):
    if comment.cons_status not in EDITABLE_STATUS_LIST:
        return Permission(need.impossible)

    if comment.cons_status == APPROVED_STATUS:
        return Denial(need.everybody)

    elif comment.cons_user_id:
        return Permission(need.admin, need.user_id(comment.cons_user_id))

    else:
        return Permission(need.admin)


def perm_edit_record(record):
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
        elif isinstance(v, list):
            rv[k] = v
        else:
            rv[k] = '' if v is None else unicode(v)
    return rv


def json_encode_more(value):
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, datetime):
        return value.isoformat()

    raise TypeError


class IndexMixin(object):

    def get_map_url(self, subject_code, region_code=None):
        map_colors = [
            {
                'region': record_region_core,
                'code': CONCLUSION_COLOR.get(record_status),
            }
            for record_status, record_region_core in
            self.dataset.get_assessment_for_all_regions(subject_code)
            if region_code is None or record_region_core == region_code
        ]
        return self.map_url_template.format(**{
            self.subject_name: subject_code,
            'regions': urllib.quote(flask.json.dumps(map_colors)),
        })


class IndexView(flask.views.View, IndexMixin):

    def dispatch_request(self):
        subject_code = flask.request.args[self.subject_name]
        region_code = flask.request.args['region']

        subject = self.dataset.get_subject(subject_code)
        region = dal.get_biogeo_region(region_code)

        if subject is None or region is None:
            flask.abort(404)

        reply_counts = self.dataset.get_reply_counts()

        topic = {'comments': []}

        for record in self.dataset.get_topic_records(subject, region):
            if record.cons_role == 'assessment':
                topic['assessment'] = self.parse_record(record)

            else:
                if not record.cons_deleted:
                    r = self.parse_record(record, is_comment=True)
                    topic['comments'].append(r)

        comment_next = self.get_comment_next_url(subject_code, region_code)

        return flask.render_template('common/indexpage.html', **{
            'subject': subject,
            'region': region,
            'topic_template': self.topic_template,
            'comment_next': comment_next,
            'blueprint': self.blueprint,
            'topic': topic,
            'reply_counts': reply_counts,
            'map_url': self.get_map_url(subject.code),
            'dashboard_url': self.get_dashboard_url(subject),
        })


class RecordView(IndexMixin, flask.views.View):

    methods = ['GET', 'POST']

    def dispatch_request(self, record_id=None, comment_id=None,
                         dataset_id=None):

        self.dataset_id = dataset_id
        self.setup_record_and_form(record_id=record_id, comment_id=comment_id)

        self.setup_template_context()
        self.template_ctx['next_url'] = flask.request.args.get('next') or \
                                        self.get_next_url()
        self.template_ctx['blueprint'] = self.blueprint
        self.template_ctx['record_id'] = self.record.id

        if flask.request.method == 'POST' and self.form.validate():
            self.flatten_commentform(self.form.data, self.object)

            models.db.session.add(self.object)

            app = flask.current_app._get_current_object()
            if self.new_record:
                self.add_signal.send(app, ob=self.object,
                                          new_data=self.form.data)
            else:
                self.edit_signal.send(app, ob=self.object,
                                      old_data=self.original_data, new_data=self.form.data)

            models.db.session.commit()

            self.dataset.update_extra_fields(self.form.data, self.object)
            return flask.render_template(self.template_saved,
                                         **self.template_ctx)

        self.template_ctx['form'] = self.form
        self.template_ctx['new_comment'] = self.new_record
        self.template_ctx['template_base'] = self.template_base

        addform_pressure = forms.PressureForm(prefix='addform_pressure.')
        addform_measure = forms.MeasuresForm(prefix='addform_measure.')
        self.template_ctx.update({
                'addform_pressure': addform_pressure,
                'addform_threat': forms.PressureForm(prefix='addform_threat.'),
                'addform_measure': addform_measure,
                'PRESSURES': dict(addform_pressure.pressure.choices),
                'MEASURES': dict(addform_measure.measurecode.choices)})
        return flask.render_template(self.template, **self.template_ctx)


class CommentViewMixin(object):

    template_base = "common/comment.html"

    def setup_record_and_form(self, record_id=None, comment_id=None):
        if record_id:
            self.new_record = True
            self.record = self.record_cls.query.get_or_404(record_id)
            perm_create_comment(self.record).test()
            self.object = self.comment_cls(
                cons_role='comment',
                cons_user_id=flask.g.identity.id,
                cons_date=datetime.utcnow(),
            )
            self.link_comment_to_record()
            self.form = self.form_cls(flask.request.form)

        elif comment_id:
            self.new_record = False
            self.object = self.comment_cls.query.get_or_404(comment_id)
            perm_edit_comment(self.object).test()
            self.record = self.record_for_comment(self.object)
            self.original_data = self.parse_commentform(self.object)
            if flask.request.method == 'POST':
                form_data = flask.request.form
            else:
                form_data = MultiDict(flatten_dict(self.original_data))
            self.form = self.form_cls(form_data)

        else:
            raise RuntimeError("Need at least one of "
                               "record_id and comment_id")


class CommentStateView(flask.views.View):

    methods = ['POST']

    def dispatch_request(self, comment_id):
        comment = self.dataset.get_comment(comment_id) or flask.abort(404)
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
        comment = self.dataset.get_comment(comment_id) or flask.abort(404)
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
