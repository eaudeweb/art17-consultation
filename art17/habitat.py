import urllib
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


class HabitatMixin(object):

    subject_name = 'habitat'
    blueprint = 'habitat'
    parse_record = staticmethod(schemas.parse_habitat)

    def get_records(self, habitat, region):
        records_query = (
            models.DataHabitattypeRegion.query
            .filter_by(habitat=habitat)
            .order_by(models.DataHabitattypeRegion.cons_date)
        )
        if region is not None:
            records_query = records_query.filter_by(region=region.code)

        return iter(records_query)

    @property
    def map_url_template(self):
        return flask.current_app.config['HABITAT_MAP_URL']


class HabitatIndexView(IndexView, HabitatMixin):

    template = 'habitat/index.html'
    topic_template = 'habitat/topic.html'
    subject_cls = models.DataHabitat
    record_cls = models.DataHabitattypeRegion

    def get_comment_next_url(self):
        return flask.url_for('.index', habitat=self.subject_code,
                                       region=self.region_code)

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
        'species': record.species.all(),
    })


class HabitatCommentView(CommentView, HabitatMixin):

    form_cls = forms.HabitatComment
    record_cls = models.DataHabitattypeRegion
    comment_cls = models.DataHabitattypeRegion
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
        region = models.LuBiogeoreg.query.filter_by(code=self.record.region).first_or_404()
        self.topic_list = self.get_topics(self.record.habitat, region)
        self.template_ctx = {
            'habitat': self.record.habitat,
            'record': schemas.parse_habitat(self.record),
            'map_url': self.get_map_url(region.code)
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

    def process_extra_fields(self, struct, comment):
        pass


habitat.add_url_rule('/habitate/detalii/<int:record_id>/comentarii',
                     view_func=HabitatCommentView.as_view('comment'))


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>',
                     view_func=HabitatCommentView.as_view('comment_edit'))


class HabitatCommentStateView(CommentStateView):

    comment_cls = models.DataHabitattypeRegion
    signal = comment_status_changed


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>/stare',
            view_func=HabitatCommentStateView.as_view('comment_status'))


class HabitatCommentDeleteView(CommentDeleteView):

    comment_cls = models.DataHabitattypeRegion
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)
    signal = comment_deleted


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>/sterge',
            view_func=HabitatCommentDeleteView.as_view('comment_delete'))
