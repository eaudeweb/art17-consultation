import flask
from blinker import Signal
from art17 import models
from art17 import dal
from art17.common import (IndexView, CommentView, CommentStateView,
                          CommentDeleteView)
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

    @property
    def map_url_template(self):
        return flask.current_app.config['SPECIES_MAP_URL']


class SpeciesIndexView(IndexView, SpeciesMixin):

    template = 'species/index.html'
    topic_template = 'species/topic.html'
    subject_cls = models.DataSpecies
    record_cls = models.DataSpeciesRegion

    def get_comment_next_url(self):
        return flask.url_for('.index', species=self.subject_code,
                                       region=self.region_code)

    def prepare_context(self):
        super(SpeciesIndexView, self).prepare_context()
        self.ctx.update({
            'species_groups': [{'id': g.code,
                                'text': g.description}
                               for g in dal.get_species_groups()],
            'annex_II': self.subject.lu.annexii == 'Y',
            'annex_IV': self.subject.lu.annexiv == 'Y',
            'annex_V': self.subject.lu.annexv == 'Y',
        })


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


class SpeciesCommentView(CommentView, SpeciesMixin):

    form_cls = forms.SpeciesComment
    record_cls = models.DataSpeciesRegion
    comment_cls = models.DataSpeciesRegion
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

    def process_extra_fields(self, struct, comment):
        for pressure in comment.get_pressures():
            models.db.session.delete(pressure)

        for pressure in struct['pressures']['pressures']:
            pressure_obj = models.DataPressuresThreats(
                species_id=comment.id,
                pressure=pressure['pressure'],
                ranking=pressure['ranking'],
                type='p',
            )
            models.db.session.add(pressure_obj)
            models.db.session.flush()
            for pollution in pressure['pollutions']:
                pollution_obj = models.DataPressuresThreatsPollution(
                    pollution_pressure_id=pressure_obj.id,
                    pollution_qualifier=pollution,
                )
                models.db.session.add(pollution_obj)

        for threat in comment.get_threats():
            models.db.session.delete(threat)

        for threat in struct['threats']['threats']:
            threat_obj = models.DataPressuresThreats(
                species_id=comment.id,
                pressure=threat['pressure'],
                ranking=threat['ranking'],
                type='t',
            )
            models.db.session.add(threat_obj)
            models.db.session.flush()
            for pollution in threat['pollutions']:
                pollution_obj = models.DataPressuresThreatsPollution(
                    pollution_pressure_id=threat_obj.id,
                    pollution_qualifier=pollution,
                )
                models.db.session.add(pollution_obj)

        for measure in comment.measures:
            models.db.session.delete(measure)

        for measure in struct['measures']['measures']:
            measure_obj = models.DataMeasures(measure_sr_id=comment.id,
                                              **measure
            )
            models.db.session.add(measure_obj)
        models.db.session.commit()


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
