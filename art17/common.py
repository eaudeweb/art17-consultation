# encoding: utf-8

import flask
import flask.views
from werkzeug.utils import cached_property
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


class GenericRecord(object):

    def __init__(self, row, is_comment=False):
        self.row = row
        self.is_comment = is_comment

    def _split_period(self, year_string):
        if year_string:
            # u2011: non-breaking hyphen
            return u"(%s\u2011%s)" % (year_string[:4], year_string[4:])
        else:
            return ""

    def _get_trend(self, name, qualifier=''):
        period = getattr(self.row, '%s_trend%s_period' % (name, qualifier))
        trend = getattr(self.row, '%s_trend%s' % (name, qualifier))
        return {
            'trend': trend,
            'period': self._split_period(period),
        }

    def _get_magnitude(self, name, qualifier=''):
        mag_min = getattr(self.row, '%s_trend%s_magnitude_min' % (name, qualifier))
        mag_max = getattr(self.row, '%s_trend%s_magnitude_max' % (name, qualifier))
        return {
            'min': mag_min,
            'max': mag_max,
        }

    def _get_conclusion(self, name):
        return getattr(self.row, 'conclusion_%s' % name)

    def _get_reference_value(self, name, ideal):
        favourable = getattr(self.row, 'complementary_favourable_%s' % name)
        favourable_op = getattr(self.row, 'complementary_favourable_%s_op' % name)
        favourable_x = getattr(self.row, 'complementary_favourable_%s_x' % name)
        method = getattr(self.row, 'complementary_favourable_%s_method' % name)

        if favourable:
            value = favourable

        elif favourable_op:
            value = "%s%s" % (favourable_op, ideal)

        elif favourable_x:
            value = "Unknown"

        else:
            value = "N/A"

        return {
            'value': value,
            'method': method,
        }

    @cached_property
    def comment(self):
        assert self.is_comment
        return {
            'user_id': self.row.user_id,
        }


class CommentView(flask.views.View):

    methods = ['GET', 'POST']

    def dispatch_request(self, record_id=None, comment_id=None):
        form = self.form_cls(flask.request.form)

        if record_id:
            self.record = self.record_cls.query.get_or_404(record_id)
            self.comment = self.comment_cls()

        elif comment_id:
            self.comment = self.comment_cls.query.get_or_404(comment_id)
            self.record = self.record_for_comment(self.comment)
            form.range.surface_area.data = self.comment.range_surface_area

        else:
            raise RuntimeError("Need at least one of record_id and comment_id")

        self.setup_template_context()
        self.template_ctx['next_url'] = flask.request.args.get('next')

        if flask.request.method == 'POST' and form.validate():
            self.link_comment_to_record()
            self.comment.user_id = flask.g.identity.id

            form.populate_obj(self.comment)

            models.db.session.add(self.comment)
            models.db.session.commit()

            return flask.render_template(self.template_saved,
                                         **self.template_ctx)

        self.template_ctx['form'] = form
        return flask.render_template(self.template, **self.template_ctx)
