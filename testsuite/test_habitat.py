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
    'pressures': {
        'pressures_method': '1',
    },
    'threats': {
        'threats_method': '1',
    },
    'measures': {},
    'natura2000': {
        'area': {
            'min': 0,
            'max': 100,
        },
        'method': '',
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
    'report_observation': 'nothing to add',
    'published': 'someday',
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
    'pressures_method': '1',
    'threats_method': '1',
    'natura2000_area_min': 0,
    'natura2000_area_max': 100,
    'natura2000_area_method': '',
    'natura2000_area_trend': '+',
    'conclusion_area': 'U2',
    'conclusion_area_trend': '+',

    'conclusion_structure': 'U2',
    'conclusion_structure_trend': '+',

    'conclusion_future': 'U2',
    'conclusion_future_trend': '+',

    'conclusion_assessment': 'U2',
    'conclusion_assessment_trend': '+',

    'cons_report_observation': 'nothing to add',

    'published': 'someday',
}


def _create_habitat_record(habitat_app, comment=False):
    from art17 import models
    with habitat_app.app_context():
        habitat = models.DataHabitat(id=1, code='1234')
        habitat.lu = models.LuHabitattypeCodes(objectid=1, code=1234)
        record = models.DataHabitattypeRegion(
            id=1,
            habitat=habitat,
            cons_role='assessment',
            region='ALP',
        )
        record.lu = models.LuBiogeoreg(objectid=1)
        models.db.session.add(record)

        if comment:
            comment = models.DataHabitattypeRegion(
                id=2,
                habitat_id=1,
                cons_role='comment',
                cons_user_id='smith',
                region='ALP',
                range_surface_area=1337,
                cons_dataset_id=1,
            )
            models.db.session.add(comment)

        models.db.session.commit()


def test_load_comments_view(habitat_app):
    _create_habitat_record(habitat_app)
    client = habitat_app.test_client()
    resp = client.get('/habitate/detalii/1/comentarii')
    assert resp.status_code == 200


def test_save_comment_record(habitat_app):
    from art17.models import DataHabitattypeRegion
    habitat_app.config['TESTING_USER_ID'] = 'smith'
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
        comment = DataHabitattypeRegion.query.get(2)
        assert comment.cons_role == 'comment'
        assert comment.cons_user_id == 'smith'
        assert comment.habitat.code == '1234'
        assert comment.region == 'ALP'
        assert comment.range_surface_area == 50


def test_edit_comment_form(habitat_app):
    _create_habitat_record(habitat_app, comment=True)
    client = habitat_app.test_client()
    resp1 = client.get('/habitate/comentarii/f3b4c23bcb88')
    assert resp1.status_code == 404
    resp2 = client.get('/habitate/comentarii/2')
    assert resp2.status_code == 200
    assert '1337' in resp2.data


def test_edit_comment_submit(habitat_app):
    from art17.models import DataHabitattypeRegion
    _create_habitat_record(habitat_app, comment=True)
    client = habitat_app.test_client()
    resp = client.post('/habitate/comentarii/2',
                       data={'range.surface_area': '50',
                             'range.method': '1',
                             'coverage.surface_area': 123,
                             'coverage.date': '2001',
                             'coverage.method': '1'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with habitat_app.app_context():
        comment = DataHabitattypeRegion.query.get(2)
        assert comment.range_surface_area == 50


def test_extra_fields_save(habitat_app):
    import json
    from art17.models import DataHabitattypeRegion, LuThreats, LuRanking, LuPollution
    from art17 import models
    habitat_app.config['TESTING_USER_ID'] = 'smith'
    _create_habitat_record(habitat_app)
    with habitat_app.app_context():
        pressure = LuThreats(code='1')
        ranking = LuRanking(code='M')
        pollution = LuPollution(code='A')
        models.db.session.add(pressure)
        models.db.session.add(ranking)
        models.db.session.add(pollution)
        models.db.session.commit()
    pressure_data = json.dumps({'pressure': '1', 'ranking': 'M', 'pollutions': ['A']})
    measure_data = json.dumps({'measurecode': '1', 'rankingcode': 'M'})
    client = habitat_app.test_client()
    resp = client.post('/habitate/detalii/1/comentarii',
                       data={'pressures.pressures': [pressure_data],
                             'measures.measures': [measure_data]})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with habitat_app.app_context():
        comment = DataHabitattypeRegion.query.get(2)
        assert comment.cons_role == 'comment'
        assert comment.cons_user_id == 'smith'
        assert len(list(comment.pressures)) == 1
        assert comment.pressures[0].pressure == '1'
        assert comment.pressures[0].ranking == 'M'
        assert comment.pressures[0].pollutions[0].pollution_qualifier == 'A'
        assert comment.measures[0].measurecode == '1'


def test_one_field_required(habitat_app):
    from werkzeug.datastructures import MultiDict
    from art17 import forms
    with habitat_app.app_context():
        form = forms.HabitatComment(MultiDict())
        assert not form.validate()


def test_save_all_form_fields(habitat_app):
    from art17 import forms
    from art17 import models
    from art17.common import flatten_dict
    from art17.schemas import flatten_habitat_commentform
    from werkzeug.datastructures import MultiDict

    form_data = MultiDict(flatten_dict(HABITAT_STRUCT_DATA))

    with habitat_app.app_context():
        form = forms.HabitatComment(form_data)
        assert form.validate()

    comment = models.DataHabitattypeRegion()
    flatten_habitat_commentform(form.data, comment)

    for k, v in HABITAT_MODEL_DATA.items():
        assert getattr(comment, k) == v


def test_flatten():
    from art17.schemas import flatten_habitat_commentform
    from art17 import models
    obj = models.DataHabitattypeRegion()
    flatten_habitat_commentform(HABITAT_STRUCT_DATA, obj)
    for k, v in HABITAT_MODEL_DATA.items():
        assert getattr(obj, k) == v


def test_parse():
    from art17.schemas import parse_habitat_commentform
    from art17 import models
    obj = models.DataHabitattypeRegion(**HABITAT_MODEL_DATA)
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
    page = client.get('/replici/habitate/2')
    form = page.forms['reply-form']
    form['text'] = "hello world!"
    form.submit()

    with habitat_app.app_context():
        replies = models.CommentReply.query.all()
        assert len(replies) == 1
        msg = replies[0]
        assert msg.text == "hello world!"
        assert msg.user_id == 'somewho'
        assert msg.parent_table == 'habitat'
        assert msg.parent_id == '2'


def test_permissions(habitat_app):
    from art17 import models, common
    from flask.ext.principal import RoleNeed, UserNeed
    _create_habitat_record(habitat_app, comment=True)

    with habitat_app.app_context():
        row = models.DataHabitattypeRegion.query.get(1)
        comment = models.DataHabitattypeRegion.query.get(2)

        assert common.perm_create_comment(row).needs == set([
            RoleNeed('admin'),
            RoleNeed('expert'),
            RoleNeed('expert:habitat'),
            RoleNeed('expert:habitat:1234'),
        ])

        assert common.perm_edit_comment(comment).needs == set([
            RoleNeed('admin'),
            UserNeed('smith'),
        ])

        assert common.perm_update_comment_status(comment).needs == set([
            RoleNeed('admin'),
            RoleNeed('reviewer'),
            RoleNeed('reviewer:habitat'),
            RoleNeed('reviewer:habitat:1234'),
        ])

        assert common.perm_delete_comment(comment).needs == set([
            RoleNeed('admin'),
            UserNeed('smith'),
        ])
