import flask
from sqlalchemy import func
from blinker import Signal
from art17 import models
from art17.common import IndexView, CommentView, CommentStateView
from art17.schemas import parse_species
from art17 import forms
from art17 import schemas

species = flask.Blueprint('species', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()


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

    def custom_stuff(self):
        if self.subject_code:
            self.subject = (self.subject_cls.query
                        .filter_by(code=self.subject_code)
                        .join(models.DataSpecies.lu)
                        .first_or_404())
        else:
            self.subject = None

        self.region_code = flask.request.args.get('region', '')
        if self.region_code:
            self.region = (models.LuBiogeoreg.query
                        .filter_by(code=self.region_code)
                        .first_or_404())
        else:
            self.region = None

        if self.subject:
            records = self.subject.regions
            comments = self.subject.comments

            if self.region:
                records = records.filter_by(region=self.region.code)
                comments = comments.filter_by(region=self.region.code)

            CommentMessage = models.CommentMessage
            message_counts = dict(models.db.session.query(
                                    CommentMessage.parent,
                                    func.count(CommentMessage.id)
                                ).group_by(CommentMessage.parent))

        species_list = self.subject_cls.query.join(self.record_cls)

        group_code = flask.request.args.get('group')

        self.ctx = {
            'species_groups': [{'id': g.code,
                                'text': g.description}
                               for g in models.LuGrupSpecie.query],
            'current_group_code': group_code,
            'species_list': [{'id': s.code,
                              'group_id': s.lu.group_code,
                              'text': s.lu.speciesname}
                             for s in species_list],
            'current_species_code': self.subject_code,
            'current_region_code': self.region_code,

            'species': None if self.subject is None else {
                'code': self.subject.code,
                'name': self.subject.lu.speciesname,
                'annex_II': self.subject.lu.annexii == 'Y',
                'annex_IV': self.subject.lu.annexiv == 'Y',
                'annex_V': self.subject.lu.annexv == 'Y',
                'records': [parse_species(r) for r in records],
                'comments': [parse_species(r, is_comment=True) for r in comments],
                'message_counts': message_counts,
            },
        }


species.add_url_rule('/specii/', view_func=SpeciesIndexView.as_view('index'))


@species.route('/specii/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataSpeciesRegion.query.get_or_404(record_id)
    return flask.render_template('species/detail.html', **{
        'species': record.species,
        'record': parse_species(record),
    })


class SpeciesCommentView(CommentView):

    form_cls = forms.SpeciesComment
    record_cls = models.DataSpeciesRegion
    comment_cls = models.DataSpeciesComment
    parse_commentform = staticmethod(schemas.parse_species_commentform)
    flatten_commentform = staticmethod(schemas.flatten_species_commentform)
    template = 'species/comment.html'
    template_saved = 'species/comment-saved.html'
    add_signal = comment_added
    edit_signal = comment_edited

    def link_comment_to_record(self):
        self.comment.species_id = self.record.species_id
        self.comment.region = self.record.region

    def setup_template_context(self):
        self.template_ctx = {
            'species': self.record.species,
            'record': parse_species(self.record),
        }

    def record_for_comment(self, comment):
        records = (models.DataSpeciesRegion.query
                            .filter_by(species_id=comment.species_id)
                            .filter_by(region=comment.region)
                            .all())
        assert len(records) == 1, "Expected exactly one record for the comment"
        return records[0]


species.add_url_rule('/specii/detalii/<int:record_id>/comentariu',
                     view_func=SpeciesCommentView.as_view('comment'))


species.add_url_rule('/specii/comentariu/<comment_id>',
                     view_func=SpeciesCommentView.as_view('comment_edit'))


class SpeciesCommentStateView(CommentStateView):

    comment_cls = models.DataSpeciesComment
    signal = comment_status_changed


species.add_url_rule('/specii/comentariu/<comment_id>/stare',
                view_func=SpeciesCommentStateView.as_view('comment_status'))
