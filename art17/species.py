import flask
from blinker import Signal
from art17 import models
from art17.common import (IndexView, CommentView, CommentStateView,
                          CommentDeleteView)
from art17 import forms
from art17 import schemas

species = flask.Blueprint('species', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()
comment_deleted = Signal()


@species.route('/specii/regiuni/<int:species_code>')
def lookup_regions(species_code):
    species = (models.DataSpecies.query
                .filter_by(code=species_code)
                .first_or_404())
    regions = [{'id': r.lu.code, 'text': r.lu.name_ro}
               for r in species.regions.join(models.DataSpeciesRegion.lu)]
    return flask.jsonify(options=regions)


class SpeciesIndexView(IndexView):

    template = 'species/index.html'
    subject_name = 'species'
    subject_cls = models.DataSpecies
    record_cls = models.DataSpeciesRegion
    parse_record = staticmethod(schemas.parse_species)
    blueprint = 'species'

    def parse_request(self):
        super(SpeciesIndexView, self).parse_request()
        self.group_code = self.subject.lu.group_code

    def get_comment_next_url(self):
        return flask.url_for('.index', species=self.subject_code,
                                       region=self.region_code)

    @property
    def map_url_template(self):
        return flask.current_app.config['SPECIES_MAP_URL']

    def prepare_context(self):
        super(SpeciesIndexView, self).prepare_context()
        self.ctx.update({
            'species_groups': [{'id': g.code,
                                'text': g.description}
                               for g in models.LuGrupSpecie.query],
            'current_group_code': self.group_code,
        })

        if self.subject:
            self.ctx.update({
                'annex_II': self.subject.lu.annexii == 'Y',
                'annex_IV': self.subject.lu.annexiv == 'Y',
                'annex_V': self.subject.lu.annexv == 'Y',
            })

    def get_subject_list(self):
        return [{'id': s.code,
                 'group_id': s.lu.group_code,
                 'text': s.lu.display_name}
                for s in self.subject_list]


species.add_url_rule('/specii/', view_func=SpeciesIndexView.as_view('index'))


@species.route('/specii/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataSpeciesRegion.query.get_or_404(record_id)
    return flask.render_template('species/detail.html', **{
        'species': record.species,
        'record': schemas.parse_species(record),
        'pressures': record.pressures.all(),
    })


class SpeciesCommentView(CommentView):

    form_cls = forms.SpeciesConclusion
    record_cls = models.DataSpeciesRegion
    comment_cls = models.DataSpeciesComment
    parse_commentform = staticmethod(schemas.parse_species_conclusionform)
    flatten_commentform = staticmethod(schemas.flatten_species_conclusionform)
    template = 'species/conclusion.html'
    template_saved = 'species/conclusion-saved.html'
    add_signal = comment_added
    edit_signal = comment_edited

    def link_comment_to_record(self):
        self.comment.species_id = self.record.species_id
        self.comment.region = self.record.region

    def setup_template_context(self):
        self.template_ctx = {
            'species': self.record.species,
            'record': schemas.parse_species(self.record),
        }

    def record_for_comment(self, comment):
        records = (models.DataSpeciesRegion.query
                            .filter_by(species_id=comment.species_id)
                            .filter_by(region=comment.region)
                            .all())
        assert len(records) == 1, ("Expected exactly one record "
                                   "for the comment")
        return records[0]


species.add_url_rule('/specii/detalii/<int:record_id>/concluzii',
                     view_func=SpeciesCommentView.as_view('conclusion'))


species.add_url_rule('/specii/concluzii/<comment_id>',
                 view_func=SpeciesCommentView.as_view('conclusion_edit'))


class SpeciesCommentStateView(CommentStateView):

    comment_cls = models.DataSpeciesComment
    signal = comment_status_changed


species.add_url_rule('/specii/concluzii/<comment_id>/stare',
            view_func=SpeciesCommentStateView.as_view('conclusion_status'))


class SpeciesCommentDeleteView(CommentDeleteView):

    comment_cls = models.DataSpeciesComment
    parse_commentform = staticmethod(schemas.parse_species_conclusionform)
    signal = comment_deleted


species.add_url_rule('/specii/concluzii/<comment_id>/sterge',
            view_func=SpeciesCommentDeleteView.as_view('conclusion_delete'))
