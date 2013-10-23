import flask
from blinker import Signal
from art17 import models
from art17.common import (IndexView, ConclusionView, ConclusionStateView,
                          ConclusionDeleteView)
from art17 import forms
from art17 import schemas

habitat = flask.Blueprint('habitat', __name__)

conclusion_added = Signal()
conclusion_edited = Signal()
conclusion_status_changed = Signal()
conclusion_deleted = Signal()


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
    subject_name = 'habitat'
    subject_cls = models.DataHabitat
    record_cls = models.DataHabitattypeRegion
    parse_record = staticmethod(schemas.parse_habitat)
    blueprint = 'habitat'

    def get_conclusion_next_url(self):
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
        'pressures': record.pressures.all(),
    })


class HabitatConclusionView(ConclusionView):

    form_cls = forms.HabitatConclusion
    record_cls = models.DataHabitattypeRegion
    conclusion_cls = models.DataHabitattypeComment
    parse_conclusionform = staticmethod(schemas.parse_habitat_conclusionform)
    flatten_conclusionform = staticmethod(schemas.flatten_habitat_conclusionform)
    template = 'habitat/conclusion.html'
    template_saved = 'habitat/conclusion-saved.html'
    add_signal = conclusion_added
    edit_signal = conclusion_edited

    def link_conclusion_to_record(self):
        self.conclusion.habitat_id = self.record.habitat_id
        self.conclusion.region = self.record.region

    def setup_template_context(self):
        self.template_ctx = {
            'habitat': self.record.habitat,
            'record': schemas.parse_habitat(self.record),
        }

    def record_for_conclusion(self, conclusion):
        records = (models.DataHabitattypeRegion.query
                            .filter_by(habitat_id=conclusion.habitat_id)
                            .filter_by(region=conclusion.region)
                            .all())
        assert len(records) == 1, ("Expected exactly one record "
                                   "for the conclusion")
        return records[0]


habitat.add_url_rule('/habitate/detalii/<int:record_id>/concluzii',
                     view_func=HabitatConclusionView.as_view('conclusion'))


habitat.add_url_rule('/habitate/concluzii/<conclusion_id>',
                     view_func=HabitatConclusionView.as_view('conclusion_edit'))


class HabitatConclusionStateView(ConclusionStateView):

    conclusion_cls = models.DataHabitattypeComment
    signal = conclusion_status_changed


habitat.add_url_rule('/habitate/concluzii/<conclusion_id>/stare',
            view_func=HabitatConclusionStateView.as_view('conclusion_status'))


class HabitatConclusionDeleteView(ConclusionDeleteView):

    conclusion_cls = models.DataHabitattypeComment
    parse_conclusionform = staticmethod(schemas.parse_habitat_conclusionform)
    signal = conclusion_deleted


habitat.add_url_rule('/habitate/concluzii/<conclusion_id>/sterge',
            view_func=HabitatConclusionDeleteView.as_view('conclusion_delete'))
