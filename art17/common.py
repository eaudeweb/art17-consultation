# encoding: utf-8

from datetime import datetime
from dateutil import tz
from decimal import Decimal
from babel.dates import format_datetime
import flask
import flask.views
from werkzeug.datastructures import MultiDict
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
            'CONCLUSIONS': lookup.CONCLUSIONS}


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

    raise TypeError


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

            form.populate_obj(self.comment)
            models.db.session.add(self.comment)

            app = flask.current_app._get_current_object()
            if new_comment:
                self.add_signal.send(app, ob=self.comment)
            else:
                self.edit_signal.send(app, ob=self.comment, old_data=old_data)

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
        comment.status = new_status
        models.db.session.commit()
        return flask.redirect(next_url)
