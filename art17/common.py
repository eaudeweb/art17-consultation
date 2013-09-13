# encoding: utf-8

from datetime import datetime
from dateutil import tz
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

common = flask.Blueprint('common', __name__)


@common.app_context_processor
def inject_constants():
    return {'TREND_NAME': lookup.TREND_NAME,
            'METHODS_USED': lookup.METHODS_USED,
            'LU_FV_RANGE_OP': lookup.LU_FV_RANGE_OP,
            'LU_FV_RANGE_OP_FUNCT': lookup.LU_FV_RANGE_OP_FUNCT,
            'LU_POP_NUMBER': lookup.LU_POP_NUMBER,}


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


class CommentView(flask.views.View):

    methods = ['GET', 'POST']

    def dispatch_request(self, record_id=None, comment_id=None):
        if record_id:
            self.record = self.record_cls.query.get_or_404(record_id)
            self.comment = self.comment_cls(user_id=flask.g.identity.id,
                                            comment_date=datetime.utcnow())
            form = self.form_cls(flask.request.form)

        elif comment_id:
            self.comment = self.comment_cls.query.get_or_404(comment_id)
            self.record = self.record_for_comment(self.comment)
            if flask.request.method == 'POST':
                form_data = flask.request.form
            else:
                struct = self.parse_commentform(self.comment)
                form_data = MultiDict(flatten_dict(struct))
            form = self.form_cls(form_data)

        else:
            raise RuntimeError("Need at least one of record_id and comment_id")

        self.setup_template_context()
        self.template_ctx['next_url'] = flask.request.args.get('next')

        if flask.request.method == 'POST' and form.validate():
            self.link_comment_to_record()

            form.populate_obj(self.comment)

            models.db.session.add(self.comment)
            models.db.session.commit()

            return flask.render_template(self.template_saved,
                                         **self.template_ctx)

        self.template_ctx['form'] = form
        return flask.render_template(self.template, **self.template_ctx)
