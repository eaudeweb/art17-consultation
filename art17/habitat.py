import flask
from blinker import Signal
from art17 import models
from art17.common import (IndexView, CommentView, CommentStateView,
                          CommentDeleteView)
from art17 import forms
from art17 import schemas

habitat = flask.Blueprint('habitat', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()
comment_deleted = Signal()


@habitat.route('/habitate/regiuni/<int:habitat_code>')
def lookup_regions(habitat_code):
    habitat = (models.DataHabitat.query
                .filter_by(code=habitat_code)
                .first_or_404())
    regions = [{'id': r.lu.code, 'text': r.lu.name_ro}
               for r in habitat.regions.join(models.DataHabitattypeRegion.lu)]
    return flask.jsonify(options=regions)


class HabitatIndexView(IndexView):

    template = 'habitat/index.html'
    topic_template = 'habitat/topic.html'
    subject_name = 'habitat'
    subject_cls = models.DataHabitat
    record_cls = models.DataHabitattypeRegion
    blueprint = 'habitat'

    def get_topics(self, habitat, region):
        topics_query = (
            models.Topic.query
            .join(models.Topic.habitat_assessment)
            .join(models.Topic.region)
            .filter(models.Topic.habitat == habitat)
        )
        if region is not None:
            topics_query = topics_query.filter(models.Topic.region == region)

        for topic in topics_query:
            yield {
                'region': topic.region,
                'assessment': schemas.parse_habitat(topic.habitat_assessment),
                'comments': [schemas.parse_habitat(c, is_comment=True)
                             for c in
                             topic.habitat_comments.filter_by(deleted=False)],
            }

    def get_comment_next_url(self):
        return flask.url_for('.index', habitat=self.subject_code,
                                       region=self.region_code)

    @property
    def map_url_template(self):
        return flask.current_app.config['HABITAT_MAP_URL']

    def get_subject_list(self):
        return [{'id': h.code, 'text': h.lu.display_name}
                for h in self.subject_list]


habitat.add_url_rule('/habitate/', view_func=HabitatIndexView.as_view('index'))


@habitat.route('/habitate/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)
    return flask.render_template('habitat/detail.html', **{
        'habitat': record.habitat,
        'record': schemas.parse_habitat(record),
        'pressures': record.pressures.filter_by(type='p').all(),
        'threats': record.pressures.filter_by(type='t').all(),
        'measures': record.measures.all(),
    })


class HabitatCommentView(CommentView):

    form_cls = forms.HabitatComment
    record_cls = models.DataHabitattypeRegion
    comment_cls = models.DataHabitattypeComment
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)
    flatten_commentform = staticmethod(schemas.flatten_habitat_commentform)
    template = 'habitat/comment.html'
    template_saved = 'habitat/comment-saved.html'
    add_signal = comment_added
    edit_signal = comment_edited

    def link_comment_to_record(self):
        self.comment.habitat_id = self.record.habitat_id
        self.comment.region = self.record.region

    def setup_template_context(self):
        self.template_ctx = {
            'habitat': self.record.habitat,
            'record': schemas.parse_habitat(self.record),
        }

    def record_for_comment(self, comment):
        records = (models.DataHabitattypeRegion.query
                            .filter_by(habitat_id=comment.habitat_id)
                            .filter_by(region=comment.region)
                            .all())
        assert len(records) == 1, ("Expected exactly one record "
                                   "for the conclusion")
        return records[0]


habitat.add_url_rule('/habitate/detalii/<int:record_id>/comentarii',
                     view_func=HabitatCommentView.as_view('comment'))


habitat.add_url_rule('/habitate/comentarii/<comment_id>',
                     view_func=HabitatCommentView.as_view('comment_edit'))


class HabitatCommentStateView(CommentStateView):

    comment_cls = models.DataHabitattypeComment
    signal = comment_status_changed


habitat.add_url_rule('/habitate/comentarii/<comment_id>/stare',
            view_func=HabitatCommentStateView.as_view('comment_status'))


class HabitatCommentDeleteView(CommentDeleteView):

    comment_cls = models.DataHabitattypeComment
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)
    signal = comment_deleted


habitat.add_url_rule('/habitate/comentarii/<comment_id>/sterge',
            view_func=HabitatCommentDeleteView.as_view('comment_delete'))
