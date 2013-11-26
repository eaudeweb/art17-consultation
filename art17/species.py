import flask
from blinker import Signal
from art17 import models
from art17 import dal
from art17.common import (IndexView, CommentStateView,
                          CommentDeleteView, RecordView, CommentViewMixin)
from art17 import forms
from art17 import schemas

species = flask.Blueprint('species', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()
comment_deleted = Signal()


class SpeciesMixin(object):

    subject_name = 'species'
    blueprint = 'species'
    parse_record = staticmethod(schemas.parse_species)
    dataset = dal.SpeciesDataset()
    comment_history_view = 'history.species_comments'

    @property
    def map_url_template(self):
        return flask.current_app.config['SPECIES_MAP_URL']


class SpeciesIndexView(IndexView, SpeciesMixin):

    topic_template = 'species/topic.html'

    def get_comment_next_url(self, subject_code, region_code):
        return flask.url_for('.index', species=subject_code,
                                       region=region_code)

    def get_dashboard_url(self, subject):
        return flask.url_for(
            'dashboard.species',
            group_code=subject.lu.group_code,
        )


species.add_url_rule('/specii/', view_func=SpeciesIndexView.as_view('index'))


@species.route('/specii/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataSpeciesRegion.query.get_or_404(record_id)
    return flask.render_template('species/detail.html', **{
        'species': record.species,
        'record': schemas.parse_species(record),
        'pressures': record.get_pressures().all(),
        'threats': record.get_threats().all(),
        'measures': record.measures.all(),
    })


class SpeciesCommentView(RecordView, CommentViewMixin, SpeciesMixin):

    form_cls = forms.SpeciesComment
    record_cls = models.DataSpeciesRegion
    comment_cls = models.DataSpeciesRegion
    parse_commentform = staticmethod(schemas.parse_species_commentform)
    flatten_commentform = staticmethod(schemas.flatten_species_commentform)
    template = 'species/comment.html'
    template_saved = 'species/comment-saved.html'
    add_signal = comment_added
    edit_signal = comment_edited

    def get_next_url(self):
        return flask.url_for('.index')

    def link_comment_to_record(self):
        self.object.species_id = self.record.species_id
        self.object.region = self.record.region

    def setup_template_context(self):
        self.template_ctx = {
            'species': self.record.species,
            'record': schemas.parse_species(self.record),
            'map_url': self.get_map_url(
                self.record.species.code,
                region_code=self.record.region,
            ),
        }

    def record_for_comment(self, comment):
        records = (models.DataSpeciesRegion.query
                            .filter_by(cons_role='assessment')
                            .filter_by(species_id=comment.species_id)
                            .filter_by(region=comment.region)
                            .all())
        assert len(records) == 1, ("Expected exactly one record "
                                   "for the comment")
        return records[0]


species.add_url_rule('/specii/detalii/<int:record_id>/comentarii',
                     view_func=SpeciesCommentView.as_view('comment'))


species.add_url_rule('/specii/comentarii/<int:comment_id>',
                 view_func=SpeciesCommentView.as_view('comment_edit'))


class SpeciesCommentStateView(CommentStateView):

    dataset = dal.SpeciesDataset()
    signal = comment_status_changed


species.add_url_rule('/specii/comentarii/<int:comment_id>/stare',
            view_func=SpeciesCommentStateView.as_view('comment_status'))


class SpeciesCommentDeleteView(CommentDeleteView):

    dataset = dal.SpeciesDataset()
    parse_commentform = staticmethod(schemas.parse_species_commentform)
    signal = comment_deleted


species.add_url_rule('/specii/comentarii/<int:comment_id>/sterge',
            view_func=SpeciesCommentDeleteView.as_view('comment_delete'))
