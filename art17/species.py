import flask
from werkzeug.utils import cached_property
from blinker import Signal
from art17 import models
from art17 import dal
from art17.common import (IndexView, CommentStateView,
                          CommentDeleteView, RecordView, CommentViewMixin,
                          FinalCommentMixin, DeleteDraftView,
                          CloseConsultationView, ReopenConsultationView, RedraftCommentView)
from art17 import forms
from art17 import schemas
from art17 import config

species = flask.Blueprint('species', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()
comment_submitted = Signal()
comment_finalized = Signal()
comment_deleted = Signal()


def get_dataset(dataset_id=None):
    dataset_id = dataset_id or config.get_config_value('CONSULTATION_DATASET',
                                                       '1')
    return dal.SpeciesDataset(int(dataset_id))


class SpeciesMixin(object):

    subject_name = 'species'
    blueprint = 'species'
    parse_record = staticmethod(schemas.parse_species)
    dataset = cached_property(lambda self: get_dataset())
    comment_history_view = 'history_consultation.species_comments'

    @cached_property
    def map_url_template(self):
        return config.get_config_value('SPECIES_MAP_URL')

    @cached_property
    def primary_data_url_template(self):
        return config.get_config_value('SPECIES_PRIMARY_DATA_URL')

    def get_dashboard_url(self, subject):
        if flask.current_app.testing:
            return flask.request.url
        return flask.url_for(
            'dashboard.species',
            group_code=subject.lu.group_code,
        )


class SpeciesIndexView(IndexView, SpeciesMixin):

    topic_template = 'species/topic.html'

    def get_comment_next_url(self, subject_code, region_code):
        return flask.url_for('.index', species=subject_code,
                                       region=region_code)

species.add_url_rule('/specii/', view_func=SpeciesIndexView.as_view('index'))


@species.route('/specii/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataSpeciesRegion.query.get_or_404(record_id)
    return flask.render_template('species/detail.html', **{
        'subject': record.species,
        'record': schemas.parse_species(record),
        'pressures': record.get_pressures().all(),
        'threats': record.get_threats().all(),
        'measures': record.measures.all(),
    })


class SpeciesCommentView(RecordView, CommentViewMixin, SpeciesMixin):

    form_cls = forms.SpeciesComment
    record_cls = models.DataSpeciesRegion
    parse_commentform = staticmethod(schemas.parse_species_commentform)
    flatten_commentform = staticmethod(schemas.flatten_species_commentform)
    template = 'species/comment.html'
    add_signal = comment_added
    edit_signal = comment_edited
    submit_signal = comment_submitted

    def get_next_url(self):
        if flask.current_app.testing:
            return flask.request.url
        return flask.url_for(
            '.index',
            species=self.record.species.code,
            region=self.record.region,
        )

    def setup_template_context(self):
        self.template_ctx = {
            'species': self.record.species,
            'record': schemas.parse_species(self.record),
            'map_url': self.get_map_url(
                self.record.species.code,
                region_code=self.record.region,
            ),
            'index_url': self.get_next_url(),
        }

    def record_for_comment(self, comment):
        records = (models.DataSpeciesRegion.query
                            .filter_by(cons_role='assessment')
                            .filter_by(cons_dataset_id=comment.cons_dataset_id)
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

    dataset = cached_property(lambda self: get_dataset())
    signal = comment_status_changed


species.add_url_rule('/specii/comentarii/<int:comment_id>/stare',
            view_func=SpeciesCommentStateView.as_view('comment_status'))


class SpeciesCommentDeleteView(CommentDeleteView):

    dataset = cached_property(lambda self: get_dataset())
    parse_commentform = staticmethod(schemas.parse_species_commentform)
    signal = comment_deleted


species.add_url_rule('/specii/comentarii/<int:comment_id>/sterge',
            view_func=SpeciesCommentDeleteView.as_view('comment_delete'))


class SpeciesFinalCommentView(FinalCommentMixin, SpeciesCommentView):

    signal = Signal()  # ignored


species.add_url_rule('/specii/detalii/<int:record_id>/edit_final',
                     view_func=SpeciesFinalCommentView.as_view('final_comment'))


class SpeciesDeleteDraftView(DeleteDraftView):

    dataset = cached_property(lambda self: get_dataset())


species.add_url_rule('/specii/detalii/<int:record_id>/delete_final',
                     view_func=SpeciesDeleteDraftView.as_view('delete_draft'))


class SpeciesRedraftCommentView(RedraftCommentView):

    model_cls = models.DataSpeciesRegion

species.add_url_rule('/species/redraft/<int:comment_id>',
                     view_func=SpeciesRedraftCommentView.as_view('redraft'))


class SpeciesCloseConsultationView(CloseConsultationView):

    dataset = cached_property(lambda self: get_dataset())
    parse_commentform = staticmethod(schemas.parse_species_commentform)
    flatten_commentform = staticmethod(schemas.flatten_species_commentform)
    form_cls = forms.SpeciesComment
    signal = comment_finalized

species.add_url_rule('/specii/detalii/<int:record_id>/inchide',
            view_func=SpeciesCloseConsultationView.as_view('close'))


class SpeciesReopenConsultationView(ReopenConsultationView):

    dataset = cached_property(lambda self: get_dataset())

species.add_url_rule('/specii/detalii/<int:final_record_id>/redeschide',
            view_func=SpeciesReopenConsultationView.as_view('reopen'))
