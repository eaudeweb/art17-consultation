# encoding: utf-8

from datetime import datetime
from dateutil import tz
from decimal import Decimal
from babel.dates import format_datetime
import flask
import flask.views
from werkzeug.datastructures import MultiDict
from sqlalchemy import func
from art17 import models
import lookup

DATE_FORMAT = {
    'day': 'd MMM',
    'long': 'd MMMM y HH:mm',
}

STATUS_VALUES = ['new', 'approved', 'rejected']

common = flask.Blueprint('common', __name__)


@common.app_context_processor
def inject_constants():
    return {'TREND_NAME': lookup.TREND_NAME,
            'METHODS_USED': lookup.METHODS_USED,
            'LU_FV_RANGE_OP': lookup.LU_FV_RANGE_OP,
            'LU_FV_RANGE_OP_FUNCT': lookup.LU_FV_RANGE_OP_FUNCT,
            'LU_POP_NUMBER': lookup.LU_POP_NUMBER,
            'CONCLUSIONS': lookup.CONCLUSIONS,
            'QUALITY': lookup.QUALITY}


@common.app_template_filter('local_date')
def local_date(value, format='day'):
    if not value:
        return ''
    utc = tz.gettz('UTC')
    local_tz = tz.gettz('Europe/Bucharest')
    local_value = value.replace(tzinfo=utc).astimezone(local_tz)
    return format_datetime(local_value, DATE_FORMAT[format], locale='ro')


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

    def dispatch_request(self):
        self.subject_code = flask.request.args.get(self.subject_name, type=int)

        if self.subject_code:
            self.subject = (self.subject_cls.query
                        .filter_by(code=self.subject_code)
                        .join(models.DataSpecies.lu)
                        .first_or_404())
        else:
            self.subject = None

        self.region_code = flask.request.args.get('region', '')
        if self.region_code:
            self.region = (models.LuBiogeoreg.query
                        .filter_by(code=self.region_code)
                        .first_or_404())
        else:
            self.region = None

        if self.subject:
            self.records = self.subject.regions
            self.comments = self.subject.comments

            if self.region:
                self.records = self.records.filter_by(region=self.region.code)
                self.comments = self.comments.filter_by(region=self.region.code)

            CommentMessage = models.CommentMessage
            self.message_counts = dict(models.db.session.query(
                                    CommentMessage.parent,
                                    func.count(CommentMessage.id)
                                ).group_by(CommentMessage.parent))

        self.subject_list = (self.subject_cls.query
                            .join(self.record_cls)
                            .order_by(self.subject_cls.code))

        self.ctx = {
            'subject_list': self.get_subject_list(),
            'current_subject_code': self.subject_code,
            'current_region_code': self.region_code,
        }

        if self.subject:
            self.ctx.update({
                'code': self.subject.code,
                'name': self.subject.lu.display_name,
                'records': [self.parse_record(r) for r in self.records],
                'comments': [self.parse_record(r, is_comment=True)
                             for r in self.comments],
                'message_counts': self.message_counts,
            })

        self.custom_ctx()

        return flask.render_template(self.template, **self.ctx)

    def custom_ctx(self):
        pass


class CommentView(flask.views.View):

    methods = ['GET', 'POST']

    def dispatch_request(self, record_id=None, comment_id=None):
        if record_id:
            new_comment = True
            self.record = self.record_cls.query.get_or_404(record_id)
            self.comment = self.comment_cls(user_id=flask.g.identity.id,
                                            comment_date=datetime.utcnow())
            form = self.form_cls(flask.request.form)

        elif comment_id:
            new_comment = False
            self.comment = self.comment_cls.query.get_or_404(comment_id)
            self.record = self.record_for_comment(self.comment)
            old_data = self.parse_commentform(self.comment)
            if flask.request.method == 'POST':
                form_data = flask.request.form
            else:
                form_data = MultiDict(flatten_dict(old_data))
            form = self.form_cls(form_data)

        else:
            raise RuntimeError("Need at least one of record_id and comment_id")

        self.setup_template_context()
        self.template_ctx['next_url'] = flask.request.args.get('next')

        if flask.request.method == 'POST' and form.validate():
            self.link_comment_to_record()

            self.flatten_commentform(form.data, self.comment)
            models.db.session.add(self.comment)

            app = flask.current_app._get_current_object()
            if new_comment:
                self.add_signal.send(app, ob=self.comment, new_data=form.data)
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
        old_status = comment.status
        comment.status = new_status
        app = flask.current_app._get_current_object()
        self.signal.send(app, ob=comment,
                         old_data=old_status, new_data=new_status)
        models.db.session.commit()
        return flask.redirect(next_url)
