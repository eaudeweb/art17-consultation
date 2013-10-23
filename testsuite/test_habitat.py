# encoding: utf-8

import pytest

COMMENT_SAVED_TXT = "Comentariul a fost înregistrat"
MISSING_FIELD_TXT = "Suprafața este obligatorie"

HABITAT_STRUCT_DATA = {
    'range': {
        'surface_area': 123,
        'method': '1',
        'trend_short': {
            'trend': '+',
            'period': {
                'start': '2000',
                'end': '2001',
            },
        },
        'trend_long': {
            'trend': '-',
            'period': {
                'start': '2002',
                'end': '2003',
            },
        },
        'reference_value': {
            'method': 'foo method',
            'number': 456,
            'op': '>',
            'x': None,
        },
        'conclusion': {
            'value': 'U1',
            'trend': '-',
        },
    },
    'coverage': {
        'surface_area': 123,
        'date': '2001',
        'method': '1',
        'trend_short': {
            'trend': '+',
            'period': {
                'start': '2006',
                'end': '2007',
            },
        },
        'trend_long': {
            'trend': '+',
            'period': {
                'start': '2004',
                'end': '2005',
            },
        },
        'reference_value': {
            'method': 'foo method',
            'number': 123,
            'op': '<',
            'x': None,
        },
        'conclusion': {
            'value': 'U2',
            'trend': '+',
        },
    },
    'structure': {
        'value': 'U2',
        'trend': '+',
    },
    'future_prospects': {
        'value': 'U2',
        'trend': '+',
    },
    'overall_assessment': {
        'value': 'U2',
        'trend': '+',
    },
}


HABITAT_MODEL_DATA = {
    'range_surface_area': 123,
    'range_method': '1',
    'range_trend': '+',
    'range_trend_period': '20002001',
    'range_trend_long': '-',
    'range_trend_long_period': '20022003',
    'complementary_favourable_range_op': '>',
    'complementary_favourable_range': 456,
    'complementary_favourable_range_method': 'foo method',
    'conclusion_range': 'U1',
    'conclusion_range_trend': '-',

    'coverage_surface_area': 123,
    'coverage_date': '2001',
    'coverage_method': '2001',
    'coverage_method': '1',
    'coverage_trend': '+',
    'coverage_trend_period': '20062007',
    'coverage_trend_long': '+',
    'coverage_trend_long_period': '20042005',
    'complementary_favourable_area_op': '<',
    'complementary_favourable_area': 123,
    'complementary_favourable_area_method': 'foo method',
    'conclusion_area': 'U2',
    'conclusion_area_trend': '+',

    'conclusion_structure': 'U2',
    'conclusion_structure_trend': '+',

    'conclusion_future': 'U2',
    'conclusion_future_trend': '+',

    'conclusion_assessment': 'U2',
    'conclusion_assessment_trend': '+',
}


def _create_habitat_record(habitat_app, comment=False):
    from art17 import models
    with habitat_app.app_context():
        habitat = models.DataHabitat(id=1, code='1234')
        habitat.lu = models.LuHabitattypeCodes(objectid=1, code=1234)
        record = models.DataHabitattypeRegion(id=1, habitat=habitat,
                                              region='ALP')
        record.lu = models.LuBiogeoreg(objectid=1)
        models.db.session.add(record)

        if comment:
            comment = models.DataHabitattypeComment(
                            id='4f799fdd6f5a',
                            habitat_id=1,
                            region='ALP',
                            range_surface_area=1337)
            models.db.session.add(comment)

        models.db.session.commit()


def test_load_comments_view(habitat_app):
    _create_habitat_record(habitat_app)
    client = habitat_app.test_client()
    resp = client.get('/habitate/detalii/1/comentarii')
    assert resp.status_code == 200


def test_save_comment_record(habitat_app):
    from art17.models import DataHabitattypeComment
    _create_habitat_record(habitat_app)
    client = habitat_app.test_client()
    resp = client.post('/habitate/detalii/1/comentarii',
                       data={'range.surface_area': '50',
                             'range.method': '1',
                             'coverage.surface_area': 123,
                             'coverage.date': '2001',
                             'coverage.method': '1'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with habitat_app.app_context():
        assert DataHabitattypeComment.query.count() == 1
        comment = DataHabitattypeComment.query.first()
        assert comment.habitat.code == '1234'
        assert comment.region == 'ALP'
        assert comment.range_surface_area == 50


def test_edit_comment_form(habitat_app):
    from art17.models import DataHabitattypeComment, db
    _create_habitat_record(habitat_app, comment=True)
    client = habitat_app.test_client()
    resp1 = client.get('/habitate/comentarii/f3b4c23bcb88')
    assert resp1.status_code == 404
    resp2 = client.get('/habitate/comentarii/4f799fdd6f5a')
    assert resp2.status_code == 200
    assert '1337' in resp2.data


def test_edit_comment_submit(habitat_app):
    from art17.models import DataHabitattypeComment, db
    _create_habitat_record(habitat_app, comment=True)
    client = habitat_app.test_client()
    resp = client.post('/habitate/comentarii/4f799fdd6f5a',
                       data={'range.surface_area': '50',
                             'range.method': '1',
                             'coverage.surface_area': 123,
                             'coverage.date': '2001',
                             'coverage.method': '1'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with habitat_app.app_context():
        comment = DataHabitattypeComment.query.get('4f799fdd6f5a')
        assert comment.range_surface_area == 50


def test_one_field_required():
    from werkzeug.datastructures import MultiDict
    from art17 import forms
    form = forms.HabitatComment(MultiDict())
    assert not form.validate()


def test_save_all_form_fields():
    from art17 import forms
    from art17 import models
    from art17.common import flatten_dict
    from art17.schemas import flatten_habitat_commentform
    from werkzeug.datastructures import MultiDict

    form_data = MultiDict(flatten_dict(HABITAT_STRUCT_DATA))

    form = forms.HabitatComment(form_data)
    assert form.validate()

    comment = models.DataHabitattypeComment()
    flatten_habitat_commentform(form.data, comment)

    for k, v in HABITAT_MODEL_DATA.items():
        assert getattr(comment, k) == v


def test_flatten():
    from art17.schemas import flatten_habitat_commentform
    from art17 import models
    obj = models.DataHabitattypeComment()
    flatten_habitat_commentform(HABITAT_STRUCT_DATA, obj)
    for k, v in HABITAT_MODEL_DATA.items():
        assert getattr(obj, k) == v


def test_parse():
    from art17.schemas import parse_habitat_commentform
    from art17 import models
    obj = models.DataHabitattypeComment(**HABITAT_MODEL_DATA)
    data = parse_habitat_commentform(obj)
    assert data == HABITAT_STRUCT_DATA


def test_add_comment_reply(habitat_app):
    import flask
    from webtest import TestApp
    from art17.replies import replies
    from art17 import models
    from art17.common import common

    habitat_app.config['TESTING_USER_ID'] = 'somewho'
    _create_habitat_record(habitat_app, comment=True)
    habitat_app.register_blueprint(common)
    habitat_app.register_blueprint(replies)
    client = TestApp(habitat_app)
    page = client.get('/mesaje/4f799fdd6f5a')
    form = page.forms['reply-form']
    form['text'] = "hello world!"
    form.submit()

    with habitat_app.app_context():
        replies = models.CommentReply.query.all()
        assert len(replies) == 1
        msg = replies[0]
        assert msg.text == "hello world!"
        assert msg.user_id == 'somewho'
        assert msg.parent == '4f799fdd6f5a'
