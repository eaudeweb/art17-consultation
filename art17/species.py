import flask
from sqlalchemy import func
from art17 import models
from art17.common import CommentView, CommentStateView
from art17.schemas import parse_species
from art17 import forms
from art17 import schemas

species = flask.Blueprint('species', __name__)


@species.route('/specii/regiuni/<int:species_code>')
def lookup_regions(species_code):
    species = (models.DataSpecies.query
                .filter_by(speciescode=species_code)
                .first_or_404())
    regions = [{'id': r.lu.code, 'text': r.lu.name_ro}
               for r in species.regions.join(models.DataSpeciesRegion.lu)]
    return flask.jsonify(options=regions)


@species.route('/specii/')
def index():
    group_code = flask.request.args.get('group')

    species_code = flask.request.args.get('species', type=int)
    if species_code:
        species = (models.DataSpecies.query
                    .filter_by(speciescode=species_code)
                    .join(models.DataSpecies.lu)
                    .first_or_404())
    else:
        species = None

    region_code = flask.request.args.get('region', '')
    if region_code:
        region = (models.LuBiogeoreg.query
                    .filter_by(code=region_code)
                    .first_or_404())
    else:
        region = None

    species_list = models.DataSpecies.query.join(models.DataSpeciesRegion)

    if species:
        records = species.regions
        comments = species.comments

        if region:
            records = records.filter_by(region=region.code)
            comments = comments.filter_by(region=region.code)

        CommentMessage = models.CommentMessage
        message_counts = dict(models.db.session.query(
                                CommentMessage.parent,
                                func.count(CommentMessage.id)
                            ).group_by(CommentMessage.parent))

    return flask.render_template('species/index.html', **{
        'species_groups': [{'id': g.code,
                            'text': g.description}
                           for g in models.LuGrupSpecie.query],
        'current_group_code': group_code,
        'species_list': [{'id': s.speciescode,
                          'group_id': s.lu.group_code,
                          'text': s.lu.speciesname}
                         for s in species_list],
        'current_species_code': species_code,
        'current_region_code': region_code,

        'species': None if species is None else {
            'code': species.speciescode,
            'name': species.lu.speciesname,
            'annex_II': species.lu.annexii == 'Y',
            'annex_IV': species.lu.annexiv == 'Y',
            'annex_V': species.lu.annexv == 'Y',
            'records': [parse_species(r) for r in records],
            'comments': [parse_species(r, is_comment=True) for r in comments],
            'message_counts': message_counts,
        },
    })


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
    template = 'species/comment.html'
    template_saved = 'species/comment-saved.html'

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


species.add_url_rule('/specii/comentariu/<comment_id>/stare',
                view_func=SpeciesCommentStateView.as_view('comment_status'))
