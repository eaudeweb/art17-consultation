import flask
from sqlalchemy import func
from blinker import Signal
from art17 import models
from art17.common import CommentView, CommentStateView
from art17.schemas import parse_habitat
from art17 import forms
from art17 import schemas

habitat = flask.Blueprint('habitat', __name__)

comment_added = Signal()
comment_edited = Signal()
comment_status_changed = Signal()


@habitat.route('/habitate/regiuni/<int:habitat_code>')
def lookup_regions(habitat_code):
    habitat = (models.DataHabitat.query
                .filter_by(habitatcode=habitat_code)
                .first_or_404())
    regions = [{'id': r.lu.code, 'text': r.lu.name_ro}
               for r in habitat.regions.join(models.DataHabitattypeRegion.lu)]
    return flask.jsonify(options=regions)


@habitat.route('/habitate/')
def index():
    habitat_code = flask.request.args.get('habitat', type=int)
    if habitat_code:
        habitat = (models.DataHabitat.query
                    .filter_by(habitatcode=habitat_code)
                    .join(models.DataSpecies.lu)
                    .first_or_404())
    else:
        habitat = None

    region_code = flask.request.args.get('region', '')
    if region_code:
        region = (models.LuBiogeoreg.query
                    .filter_by(code=region_code)
                    .first_or_404())
    else:
        region = None

    habitat_list = (models.DataHabitat.query
                        .join(models.DataHabitattypeRegion)
                        .order_by('habitatcode'))

    if habitat:
        records = habitat.regions
        comments = habitat.comments
        if region:
            records = records.filter_by(region=region.code)
            comments = comments.filter_by(region=region.code)

        CommentMessage = models.CommentMessage
        message_counts = dict(models.db.session.query(
                                CommentMessage.parent,
                                func.count(CommentMessage.id)
                            ).group_by(CommentMessage.parent))

    return flask.render_template('habitat/index.html', **{
        'habitat_list': [{'id': h.habitatcode, 'text': h.lu.hd_name}
                         for h in habitat_list],
        'current_habitat_code': habitat_code,
        'current_region_code': region_code,

        'habitat': None if habitat is None else {
            'name': habitat.lu.hd_name,
            'code': habitat.habitatcode,
            'records': [parse_habitat(r) for r in records],
            'comments': [parse_habitat(r, is_comment=True) for r in comments],
            'message_counts': message_counts,
        },
    })


@habitat.route('/habitate/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)
    return flask.render_template('habitat/detail.html', **{
        'habitat': record.hr_habitat,
        'record': parse_habitat(record),
    })


class HabitatCommentView(CommentView):

    form_cls = forms.HabitatComment
    record_cls = models.DataHabitattypeRegion
    comment_cls = models.DataHabitattypeComment
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
            'habitat': self.record.hr_habitat,
            'record': parse_habitat(self.record),
        }

    def record_for_comment(self, comment):
        records = (models.DataHabitattypeRegion.query
                            .filter_by(habitat_id=comment.habitat_id)
                            .filter_by(region=comment.region)
                            .all())
        assert len(records) == 1, "Expected exactly one record for the comment"
        return records[0]


habitat.add_url_rule('/habitate/detalii/<int:record_id>/comentariu',
                     view_func=HabitatCommentView.as_view('comment'))


habitat.add_url_rule('/habitate/comentariu/<comment_id>',
                     view_func=HabitatCommentView.as_view('comment_edit'))


class HabitatCommentStateView(CommentStateView):

    comment_cls = models.DataHabitattypeComment
    signal = comment_status_changed


habitat.add_url_rule('/habitate/comentariu/<comment_id>/stare',
                view_func=HabitatCommentStateView.as_view('comment_status'))
