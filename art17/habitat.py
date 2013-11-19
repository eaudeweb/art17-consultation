import urllib
import flask
from blinker import Signal
from art17 import models
from art17 import dal
from art17.common import (IndexView, CommentView, CommentStateView,
                          CommentDeleteView)
from art17 import forms
from art17 import schemas

habitat = flask.Blueprint('habitat', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()
comment_deleted = Signal()


class HabitatMixin(object):

    subject_name = 'habitat'
    blueprint = 'habitat'
    parse_record = staticmethod(schemas.parse_habitat)
    dataset = dal.HabitatDataset()

    @property
    def map_url_template(self):
        return flask.current_app.config['HABITAT_MAP_URL']


class HabitatIndexView(IndexView, HabitatMixin):

    topic_template = 'habitat/topic.html'
    subject_cls = models.DataHabitat
    record_cls = models.DataHabitattypeRegion

    def get_comment_next_url(self):
        return flask.url_for('.index', habitat=self.subject_code,
                                       region=self.region_code)


habitat.add_url_rule('/habitate/', view_func=HabitatIndexView.as_view('index'))


@habitat.route('/habitate/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)
    return flask.render_template('habitat/detail.html', **{
        'habitat': record.habitat,
        'record': schemas.parse_habitat(record),
        'pressures': record.get_pressures().all(),
        'threats': record.get_threats().all(),
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
        self.template_ctx = {
            'habitat': self.record.habitat,
            'record': schemas.parse_habitat(self.record),
            'map_url': self.get_map_url(
                self.record.habitat.code,
                region_code=self.record.region,
            ),
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
        for pressure in comment.get_pressures():
            models.db.session.delete(pressure)

        for pressure in struct['pressures']['pressures']:
            pressure_obj = models.DataPressuresThreats(
                habitat_id=comment.id,
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
                habitat_id=comment.id,
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
            measure_obj = models.DataMeasures(
                measure_hr_id=comment.id, **measure
            )
            models.db.session.add(measure_obj)
        models.db.session.commit()


habitat.add_url_rule('/habitate/detalii/<int:record_id>/comentarii',
                     view_func=HabitatCommentView.as_view('comment'))


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>',
                     view_func=HabitatCommentView.as_view('comment_edit'))


class HabitatCommentStateView(CommentStateView):

    dataset = dal.HabitatDataset()
    signal = comment_status_changed


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>/stare',
            view_func=HabitatCommentStateView.as_view('comment_status'))


class HabitatCommentDeleteView(CommentDeleteView):

    dataset = dal.HabitatDataset()
    parse_commentform = staticmethod(schemas.parse_habitat_commentform)
    signal = comment_deleted


habitat.add_url_rule('/habitate/comentarii/<int:comment_id>/sterge',
            view_func=HabitatCommentDeleteView.as_view('comment_delete'))
