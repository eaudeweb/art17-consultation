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
from art17.auth import need, admin_permission
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
    full_name = '%s:%s' % (role_base, comment.subject_identifier)
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


def perm_edit_final(subject):
    return Permission(need.admin)


common = flask.Blueprint('common', __name__)


@common.app_context_processor
def inject_permissions():
    return {
        'perm_create_comment': perm_create_comment,
        'perm_edit_comment': perm_edit_comment,
        'perm_update_comment_status': perm_update_comment_status,
        'perm_delete_comment': perm_delete_comment,
        'perm_view_history': admin_permission,
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
        final_record = None
        final_draft_record = None

        for record in self.dataset.get_topic_records(subject, region.code):
            if record.cons_role == 'assessment':
                topic['assessment'] = self.parse_record(record)

            elif record.cons_role == 'comment':
                if not record.cons_deleted:
                    r = self.parse_record(record, is_comment=True)
                    topic['comments'].append(r)

            elif record.cons_role == 'final-draft':
                final_draft_record = record

            elif record.cons_role == 'final':
                final_record = record

        comment_next = self.get_comment_next_url(subject_code, region_code)
        final_comment_url = flask.url_for(
            self.blueprint + '.final_comment',
            record_id=topic['assessment']['id'],
            next=comment_next,
        )

        close_consultation_url = flask.url_for(
            self.blueprint + '.close',
            record_id=topic['assessment']['id'],
            next=comment_next,
        )
        if final_record is not None:
            reopen_consultation_url = flask.url_for(
                self.blueprint + '.reopen',
                final_record_id=final_record.id,
                next=comment_next,
            )
        else:
            reopen_consultation_url = None

        if final_draft_record is not None:
            delete_draft_url = flask.url_for(
                self.blueprint + '.delete_draft',
                record_id=final_draft_record.id,
                next=comment_next,
            )
        else:
            delete_draft_url = None

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
            'comment_history_view': self.comment_history_view,
            'final_comment_url': final_comment_url,
            'delete_draft_url': delete_draft_url,
            'close_consultation_url': close_consultation_url,
            'perm_edit_final_for_this': perm_edit_final(subject),
            'reopen_consultation_url': reopen_consultation_url,
            'finalized': final_record is not None,
        })


class RecordView(IndexMixin, flask.views.View):

    methods = ['GET', 'POST']
    success_message = u"Comentariul a fost înregistrat."

    def dispatch_request(self, record_id=None, comment_id=None,
                         dataset_id=None):

        self.dataset_id = dataset_id
        self.setup_record_and_form(record_id=record_id, comment_id=comment_id)

        self.setup_template_context()
        next_url = flask.request.args.get('next') or self.get_next_url()
        self.template_ctx['blueprint'] = self.blueprint
        self.template_ctx['record_id'] = self.record.id
        self.template_ctx['subject'] = self.record.subject

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
            flask.flash(self.success_message, 'success')
            return flask.redirect(next_url)

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

    template_base = 'common/comment.html'
    template_saved = 'common/comment-saved.html'

    def setup_record_and_form(self, record_id=None, comment_id=None):
        if record_id:
            self.new_record = True
            self.record = self.record_cls.query.get_or_404(record_id)
            perm_create_comment(self.record).test()
            self.object = self.dataset.create_record(cons_role='comment')
            self.dataset.link_to_record(self.object, self.record)
            self.form = self.form_cls(flask.request.form)

        elif comment_id:
            self.new_record = False
            self.object = self.dataset.get_comment(comment_id) or flask.abort(404)
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


class FinalCommentMixin(object):

    success_message = u"Modificările au fost înregistrate."

    def setup_record_and_form(self, record_id=None, comment_id=None):
        self.record = self.record_cls.query.get_or_404(record_id)
        perm_edit_final(self.record.subject).test()

        row_list = self.dataset.get_topic_records(
            subject=self.record.subject,
            region_code=self.record.region,
        )
        self.object = None
        for row in row_list:
            if row.cons_role == 'final-draft':
                self.object = row

        if self.object is None:
            self.new_record = True
            self.object = self.dataset.create_record(cons_role='final-draft')
            data = self.parse_commentform(self.record)
            self.flatten_commentform(data, self.object)
            self.dataset.link_to_record(self.object, self.record)

        else:
            self.new_record = False
            self.record = self.record_for_comment(self.object)
            data = self.parse_commentform(self.object)
            self.original_data = data

        if flask.request.method == 'POST':
            form_data = flask.request.form
        else:
            form_data = MultiDict(flatten_dict(data))
        self.form = self.form_cls(form_data)


class CloseConsultationView(flask.views.View):

    methods = ['POST']

    def dispatch_request(self, record_id):
        next_url = flask.request.args['next']
        self.record = self.dataset.get_comment(record_id) or flask.abort(404)
        perm_edit_final(self.record.subject).test()

        row_list = self.dataset.get_topic_records(
            subject=self.record.subject,
            region_code=self.record.region,
        )
        self.assessment = None
        self.draft = None
        for row in row_list:
            if row.cons_role == 'assessment':
                self.assessment = row
            elif row.cons_role == 'final-draft':
                self.draft = row
            elif row.cons_role == 'final':
                raise RuntimeError("This consultation is already closed")

        if self.draft is None:
            self.draft = self.dataset.create_record(
                cons_role='final-draft',
                cons_status='not-modified',
            )
            models.db.session.add(self.draft)
            self.dataset.link_to_record(self.draft, self.record)

        self.draft.cons_role = 'final'
        models.db.session.commit()

        flask.flash(u"Consultarea a fost închisă", 'success')
        return flask.redirect(next_url)


class ReopenConsultationView(flask.views.View):

    methods = ['POST']

    def dispatch_request(self, final_record_id):
        next_url = flask.request.args['next']
        self.final = self.dataset.get_comment(final_record_id) or flask.abort(404)
        perm_edit_final(self.final.subject).test()

        assert self.final.cons_role == 'final'

        if self.final.cons_status == 'not-modified':
            models.db.session.delete(self.final)

        else:
            self.final.cons_role = 'final-draft'

        models.db.session.commit()

        flask.flash(u"Consultarea a fost redeschisă", 'success')
        return flask.redirect(next_url)


class DeleteDraftView(flask.views.View):

    methods = ['POST']

    def dispatch_request(self, record_id):
        next_url = flask.request.args['next']
        self.draft = self.dataset.get_comment(record_id) or flask.abort(404)
        perm_edit_final(self.draft.subject).test()

        assert self.draft.cons_role == 'final-draft'
        models.db.session.delete(self.draft)

        models.db.session.commit()

        flask.flash(u"Modificările au fost șterse", 'success')
        return flask.redirect(next_url)


cons_manager = Manager()


@common.route('/guide')
def guide():
    return flask.render_template('common/guide.html')

