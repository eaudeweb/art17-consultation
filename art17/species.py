import flask
from blinker import Signal
from art17 import models
from art17.common import (IndexView, ConclusionView, ConclusionStateView,
                          ConclusionDeleteView)
from art17 import forms
from art17 import schemas

species = flask.Blueprint('species', __name__)

conclusion_added = Signal()
conclusion_edited = Signal()
conclusion_status_changed = Signal()


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
    records_template = 'species/records.html'

    @property
    def map_url_template(self):
        return flask.current_app.config['SPECIES_MAP_URL']

    def custom_ctx(self):
        group_code = flask.request.args.get('group')
        self.ctx.update({
            'species_groups': [{'id': g.code,
                                'text': g.description}
                               for g in models.LuGrupSpecie.query],
            'current_group_code': group_code,
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
    })


class SpeciesConclusionView(ConclusionView):

    form_cls = forms.SpeciesConclusion
    record_cls = models.DataSpeciesRegion
    conclusion_cls = models.DataSpeciesConclusion
    parse_conclusionform = staticmethod(schemas.parse_species_conclusionform)
    flatten_conclusionform = staticmethod(schemas.flatten_species_conclusionform)
    template = 'species/conclusion.html'
    template_saved = 'species/conclusion-saved.html'
    add_signal = conclusion_added
    edit_signal = conclusion_edited

    def link_conclusion_to_record(self):
        self.conclusion.species_id = self.record.species_id
        self.conclusion.region = self.record.region

    def setup_template_context(self):
        self.template_ctx = {
            'species': self.record.species,
            'record': schemas.parse_species(self.record),
        }

    def record_for_conclusion(self, conclusion):
        records = (models.DataSpeciesRegion.query
                            .filter_by(species_id=conclusion.species_id)
                            .filter_by(region=conclusion.region)
                            .all())
        assert len(records) == 1, ("Expected exactly one record "
                                   "for the conclusion")
        return records[0]


species.add_url_rule('/specii/detalii/<int:record_id>/concluzii',
                     view_func=SpeciesConclusionView.as_view('conclusion'))


species.add_url_rule('/specii/concluzii/<conclusion_id>',
                 view_func=SpeciesConclusionView.as_view('conclusion_edit'))


class SpeciesConclusionStateView(ConclusionStateView):

    conclusion_cls = models.DataSpeciesConclusion
    signal = conclusion_status_changed


species.add_url_rule('/specii/concluzii/<conclusion_id>/stare',
            view_func=SpeciesConclusionStateView.as_view('conclusion_status'))


class SpeciesConclusionDeleteView(ConclusionDeleteView):

    conclusion_cls = models.DataSpeciesConclusion
    parse_conclusionform = staticmethod(schemas.parse_species_conclusionform)


species.add_url_rule('/specii/concluzii/<conclusion_id>/sterge',
            view_func=SpeciesConclusionDeleteView.as_view('conclusion_delete'))
