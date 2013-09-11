# encoding: utf-8

import pytest
from conftest import flatten_dict

COMMENT_SAVED_TXT = "Comentariul a fost înregistrat"
MISSING_FIELD_TXT = "Suprafața este obligatorie"

HABITAT_STRUCT_DATA = {
    'range': {
        'surface_area': 123,
        'method': 'foo range method',
        'trend_short': {
            'trend': '+',
            'period': {
                'start': 'amin',
                'end': 'amax',
            },
        },
        'trend_long': {
            'trend': '-',
            'period': {
                'start': 'bmin',
                'end': 'bmax',
            },
        },
        'reference_value': {
            'op': 'foo op',
            'number': 456,
        },
        'reference_method': 'foo method',
        'conclusion': {
            'value': 'U1',
            'trend': 'foo conclusion trend',
        },
    },
}


HABITAT_MODEL_DATA = {
    'range_surface_area': 123,
    'range_method': 'foo range method',
    'range_trend': '+',
    'range_trend_period': 'aminamax',
    'range_trend_long': '-',
    'range_trend_long_period': 'bminbmax',
    'complementary_favourable_range_op': 'foo op',
    'complementary_favourable_range': 456,
    'complementary_favourable_range_method': 'foo method',
    'conclusion_range': 'U1',
    'conclusion_range_trend': 'foo conclusion trend',
}


def _create_habitat_record(habitat_app):
    from art17 import models
    with habitat_app.app_context():
        habitat = models.DataHabitat(habitat_id=1, habitatcode='1234')
        habitat.lu = models.LuHabitattypeCodes(objectid=1, code=1234)
        record = models.DataHabitattypeRegion(hr_id=1, hr_habitat=habitat,
                                              region='ALP')
        record.lu = models.LuBiogeoreg(objectid=1)
        models.db.session.add(record)
        models.db.session.commit()


def test_load_comments_view(habitat_app):
    _create_habitat_record(habitat_app)
    client = habitat_app.test_client()
    resp = client.get('/habitate/detalii/1/comentariu')
    assert resp.status_code == 200


def test_save_comment_record(habitat_app):
    from art17.models import DataHabitattypeComment
    _create_habitat_record(habitat_app)
    client = habitat_app.test_client()
    resp = client.post('/habitate/detalii/1/comentariu',
                       data={'range.surface_area': '50'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with habitat_app.app_context():
        assert DataHabitattypeComment.query.count() == 1
        comment = DataHabitattypeComment.query.first()
        assert comment.hr_habitat.habitatcode == '1234'
        assert comment.region == 'ALP'
        assert comment.range_surface_area == 50


def test_error_on_required_record(habitat_app):
    from art17.models import DataHabitattypeComment
    _create_habitat_record(habitat_app)
    client = habitat_app.test_client()
    resp = client.post('/habitate/detalii/1/comentariu',
                       data={'range.surface_area': ''})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT not in resp.data
    assert MISSING_FIELD_TXT in resp.data
    with habitat_app.app_context():
        assert DataHabitattypeComment.query.count() == 0


def test_edit_comment_form(habitat_app):
    from art17.models import DataHabitattypeComment, db
    _create_habitat_record(habitat_app)
    with habitat_app.app_context():
        comment = DataHabitattypeComment(hr_id='4f799fdd6f5a',
                                         hr_habitat_id=1,
                                         region='ALP',
                                         range_surface_area=1337)
        db.session.add(comment)
        db.session.commit()
    client = habitat_app.test_client()
    resp1 = client.get('/habitate/comentariu/f3b4c23bcb88')
    assert resp1.status_code == 404
    resp2 = client.get('/habitate/comentariu/4f799fdd6f5a')
    assert resp2.status_code == 200
    assert '1337' in resp2.data


def test_edit_comment_submit(habitat_app):
    from art17.models import DataHabitattypeComment, db
    _create_habitat_record(habitat_app)
    with habitat_app.app_context():
        comment = DataHabitattypeComment(hr_id='4f799fdd6f5a',
                                         hr_habitat_id=1,
                                         region='ALP',
                                         range_surface_area=1337)
        db.session.add(comment)
        db.session.commit()
    client = habitat_app.test_client()
    resp = client.post('/habitate/comentariu/4f799fdd6f5a',
                       data={'range.surface_area': '50'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with habitat_app.app_context():
        comment = DataHabitattypeComment.query.get('4f799fdd6f5a')
        assert comment.range_surface_area == 50


def test_save_all_form_fields():
    from art17 import forms
    from art17 import models
    from werkzeug.datastructures import MultiDict

    form_data = MultiDict(flatten_dict(HABITAT_STRUCT_DATA))

    form = forms.HabitatComment(form_data)
    assert form.validate()

    comment = models.DataHabitattypeComment()
    form.populate_obj(comment)

    for k, v in HABITAT_MODEL_DATA.items():
        assert getattr(comment, k) == v


def test_flatten():
    class Obj(object): pass
    from art17.schemas import flatten_habitat
    obj = Obj()
    flatten_habitat(HABITAT_STRUCT_DATA, obj)
    for k, v in HABITAT_MODEL_DATA.items():
        assert getattr(obj, k) == v
