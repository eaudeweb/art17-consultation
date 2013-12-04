import urllib
import flask
from blinker import Signal
from art17 import models
from art17 import dal
from art17.common import (IndexView, CommentStateView,
                          CommentDeleteView, RecordView, CommentViewMixin,
                          FinalCommentMixin, DeleteDraftView,
                          CloseConsultationView, ReopenConsultationView)
from art17 import forms
from art17 import schemas

habitat = flask.Blueprint('habitat', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()
comment_deleted = Signal()


class HabitatMixin(object):

    subject_name = 'habitat'
    blueprint = 'habitat'
    parse_record = staticmethod(schemas.parse_habitat)
    dataset = dal.HabitatDataset()
    comment_history_view = 'history.habitat_comments'

    @property
    def map_url_template(self):
        return flask.current_app.config['HABITAT_MAP_URL']


class HabitatIndexView(IndexView, HabitatMixin):

    topic_template = 'habitat/topic.html'

    def get_comment_next_url(self, subject_code, region_code):
        return flask.url_for('.index', habitat=subject_code,
                                       region=region_code)

    def get_dashboard_url(self, subject):
        return flask.url_for('dashboard.habitats')


habitat.add_url_rule('/habitate/', view_func=HabitatIndexView.as_view('index'))


@habitat.route('/habitate/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)
    return flask.render_template('habitat/detail.html', **{
        'subject': record.habitat,
        'record': schemas.parse_habitat(record),
        'pressures': record.get_pressures().all(),
        'threats': record.get_threats().all(),
        'measures': record.measures.all(),
        'species': record.species.all(),
    })


class HabitatCommentView(RecordView, CommentViewMixin, HabitatMixin):

    form_cls = forms.HabitatComment
    record_cls = models.DataHabitattypeRegion
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)
    flatten_commentform = staticmethod(schemas.flatten_habitat_commentform)
    template = 'habitat/comment.html'
    add_signal = comment_added
    edit_signal = comment_edited

    def get_next_url(self):
        if flask.current_app.testing:
            return flask.request.url
        return flask.url_for(
            '.index',
            habitat=self.record.habitat.code,
            region=self.record.region,
        )

    def setup_template_context(self):
        self.template_ctx = {
            'habitat': self.record.habitat,
            'record': schemas.parse_habitat(self.record),
            'map_url': self.get_map_url(
                self.record.habitat.code,
                region_code=self.record.region,
            ),
        }

    def record_for_comment(self, comment):
        records = (models.DataHabitattypeRegion.query
                            .filter_by(cons_role='assessment')
                            .filter_by(habitat_id=comment.habitat_id)
                            .filter_by(region=comment.region)
                            .all())
        assert len(records) == 1, ("Expected exactly one record "
                                   "for the conclusion")
        return records[0]


habitat.add_url_rule('/habitate/detalii/<int:record_id>/comentarii',
                     view_func=HabitatCommentView.as_view('comment'))


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>',
                     view_func=HabitatCommentView.as_view('comment_edit'))


class HabitatCommentStateView(CommentStateView):

    dataset = dal.HabitatDataset()
    signal = comment_status_changed


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>/stare',
            view_func=HabitatCommentStateView.as_view('comment_status'))


class HabitatCommentDeleteView(CommentDeleteView):

    dataset = dal.HabitatDataset()
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)
    signal = comment_deleted


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>/sterge',
            view_func=HabitatCommentDeleteView.as_view('comment_delete'))


class HabitatFinalCommentView(FinalCommentMixin, HabitatCommentView):

    signal = Signal()  # ignored


habitat.add_url_rule('/habitate/detalii/<int:record_id>/edit_final',
                     view_func=HabitatFinalCommentView.as_view('final_comment'))


class HabitatDeleteDraftView(DeleteDraftView):

    dataset = dal.HabitatDataset()


habitat.add_url_rule('/habitate/detalii/<int:record_id>/delete_final',
                     view_func=HabitatDeleteDraftView.as_view('delete_draft'))


class HabitatCloseConsultationView(CloseConsultationView):

    dataset = dal.HabitatDataset()
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)
    flatten_commentform = staticmethod(schemas.flatten_habitat_commentform)

habitat.add_url_rule('/habitate/detalii/<int:record_id>/inchide',
            view_func=HabitatCloseConsultationView.as_view('close'))


class HabitatReopenConsultationView(ReopenConsultationView):

    dataset = dal.HabitatDataset()

habitat.add_url_rule('/habitate/detalii/<int:final_record_id>/redeschide',
            view_func=HabitatReopenConsultationView.as_view('reopen'))
