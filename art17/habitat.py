import flask
from blinker import Signal
from art17 import models
from art17.common import IndexView, ConclusionView, ConclusionStateView
from art17 import forms
from art17 import schemas

habitat = flask.Blueprint('habitat', __name__)

conclusion_added = Signal()
conclusion_edited = Signal()
conclusion_status_changed = Signal()


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
    records_template = 'habitat/records.html'

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
        'habitat': record.hr_habitat,
        'record': schemas.parse_habitat(record),
    })


class HabitatConclusionView(ConclusionView):

    form_cls = forms.HabitatConclusion
    record_cls = models.DataHabitattypeRegion
    conclusion_cls = models.DataHabitattypeConclusion
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
            'habitat': self.record.hr_habitat,
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


habitat.add_url_rule('/habitate/detalii/<int:record_id>/comentariu',
                     view_func=HabitatConclusionView.as_view('conclusion'))


habitat.add_url_rule('/habitate/comentariu/<conclusion_id>',
                     view_func=HabitatConclusionView.as_view('conclusion_edit'))


class HabitatConclusionStateView(ConclusionStateView):

    conclusion_cls = models.DataHabitattypeConclusion
    signal = conclusion_status_changed


habitat.add_url_rule('/habitate/comentariu/<conclusion_id>/stare',
            view_func=HabitatConclusionStateView.as_view('conclusion_status'))
