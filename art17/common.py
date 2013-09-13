# encoding: utf-8

from datetime import datetime
import flask
import flask.views
from werkzeug.datastructures import MultiDict
from art17 import models


TREND_OPTIONS = [
    ('+', u"+ (În creștere)"),
    ('-', u"- (În scădere)"),
    ('0', u"0 (Stabil)"),
    ('x', u"x (Necunoscut)"),
]

TREND_NAME = dict(TREND_OPTIONS)

CONCLUSION_OPTIONS = [
    ('FV', u"FV"),
    ('U1', u"U1"),
    ('U2', u"U2"),
    ('XX', u"XX"),
]

common = flask.Blueprint('common', __name__)


@common.app_context_processor
def inject_constants():
    return {'TREND_NAME': TREND_NAME}


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
