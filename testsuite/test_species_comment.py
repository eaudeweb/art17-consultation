# encoding: utf-8

import pytest
from conftest import flatten_dict, Obj

COMMENT_SAVED_TXT = "Comentariul a fost înregistrat"
MISSING_FIELD_TXT = "Suprafața este obligatorie"

SPECIES_STRUCT_DATA = {
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
            'method': 'foo method',
            'number': 456,
            'op': 'foo op',
            'x': None,
        },
        'conclusion': {
            'value': 'U1',
            'trend': 'foo conclusion trend',
        },
    },
}


SPECIES_MODEL_DATA = {
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


def _create_species_record(species_app):
    from art17 import models
    with species_app.app_context():
        species = models.DataSpecies(species_id=1, speciescode='1234')
        species.lu = models.LuHdSpecies(objectid=1, speciescode=1234)
        record = models.DataSpeciesRegion(sr_id=1, sr_species=species,
                                          region='ALP')
        record.lu = models.LuBiogeoreg(objectid=1)
        models.db.session.add(record)
        models.db.session.commit()


def test_load_comments_view(species_app):
    _create_species_record(species_app)
    client = species_app.test_client()
    resp = client.get('/specii/detalii/1/comentariu')
    assert resp.status_code == 200


def test_save_comment_record(species_app):
    from art17.models import DataSpeciesComment
    _create_species_record(species_app)
    client = species_app.test_client()
    resp = client.post('/specii/detalii/1/comentariu',
                       data={'range.surface_area': '50'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        assert DataSpeciesComment.query.count() == 1
        comment = DataSpeciesComment.query.first()
        assert comment.sr_species.speciescode == '1234'
        assert comment.region == 'ALP'
        assert comment.range_surface_area == 50


def test_error_on_required_record(species_app):
    from art17.models import DataSpeciesComment
    _create_species_record(species_app)
    client = species_app.test_client()
    resp = client.post('/specii/detalii/1/comentariu',
                       data={'range.surface_area': ''})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT not in resp.data
    assert MISSING_FIELD_TXT in resp.data
    with species_app.app_context():
        assert DataSpeciesComment.query.count() == 0


def test_edit_comment_form(species_app):
    from art17.models import DataSpeciesComment, db
    _create_species_record(species_app)
    with species_app.app_context():
        comment = DataSpeciesComment(sr_id='4f799fdd6f5a',
                                     sr_species_id=1,
                                     region='ALP',
                                     range_surface_area=1337)
        db.session.add(comment)
        db.session.commit()
    client = species_app.test_client()
    resp1 = client.get('/specii/comentariu/f3b4c23bcb88')
    assert resp1.status_code == 404
    resp2 = client.get('/specii/comentariu/4f799fdd6f5a')
    assert resp2.status_code == 200
    assert '1337' in resp2.data


def test_edit_comment_submit(species_app):
    from art17.models import DataSpeciesComment, db
    _create_species_record(species_app)
    with species_app.app_context():
        comment = DataSpeciesComment(sr_id='4f799fdd6f5a',
                                     sr_species_id=1,
                                     region='ALP',
                                     range_surface_area=1337)
        db.session.add(comment)
        db.session.commit()
    client = species_app.test_client()
    resp = client.post('/specii/comentariu/4f799fdd6f5a',
                       data={'range.surface_area': '50'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        comment = DataSpeciesComment.query.get('4f799fdd6f5a')
        assert comment.range_surface_area == 50


def test_save_all_form_fields():
    from art17 import forms
    from art17 import models
    from werkzeug.datastructures import MultiDict

    form_data = MultiDict(flatten_dict(SPECIES_STRUCT_DATA))

    form = forms.SpeciesComment(form_data)
    assert form.validate()

    comment = models.DataSpeciesComment()
    form.populate_obj(comment)

    for k, v in SPECIES_MODEL_DATA.items():
        assert getattr(comment, k) == v


def test_flatten():
    from art17.schemas import flatten_species
    obj = Obj()
    flatten_species(SPECIES_STRUCT_DATA, obj)
    for k, v in SPECIES_MODEL_DATA.items():
        assert getattr(obj, k) == v


def test_parse():
    from art17.schemas import parse_species
    obj = Obj()
    for k, v in SPECIES_MODEL_DATA.items():
        setattr(obj, k, v)
    obj.range_trend_magnitude_min = None
    obj.range_trend_magnitude_max = None
    obj.range_trend_long_magnitude_min = None
    obj.range_trend_long_magnitude_max = None
    obj.complementary_favourable_range_x = None
    data = parse_species(obj)
    assert data == SPECIES_STRUCT_DATA
