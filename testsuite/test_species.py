# encoding: utf-8

import pytest

COMMENT_SAVED_TXT = "Comentariul a fost înregistrat"
MISSING_FIELD_TXT = "Suprafața este obligatorie"

SPECIES_STRUCT_DATA = {
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
    'population': {
        'size': {
            'population': {
                'unit': 'i',
                'min': 1,
                'max': 12,
            },
            'population_alt': {
                'unit': 'grids10x10',
                'min': 10,
                'max': 120,
            },
        },
        'method': '1',
        'trend_short': {
            'trend': '-',
            'period': {
                'start': '2008',
                'end': '2009',
            },
        },
        'trend_long': {
            'trend': '+',
            'period': {
                'start': '2010',
                'end': '2011',
            },
        },
        'reference_value': {
            'method': 'foo pop method',
            'number': 234,
            'op': '<',
            'x': None,
        },
        'conclusion': {
            'value': 'U2',
            'trend': '-',
        },
    },
    'habitat': {
        'surface_area': 100,
        'date': '2000-2001',
        'method': '3',
        'quality': '2',
        'quality_explanation': 'foo explanation',
        'trend_short': {
            'trend': '0',
            'period': {
                'start': '2004',
                'end': '2005',
            },
        },
        'trend_long': {
            'trend': '0',
            'period': {
                'start': '2006',
                'end': '2007',
            },
        },
        'area_suitable': 1000,
        'conclusion': {
            'value': 'U1',
            'trend': '-',
        },
    },
    'future_prospects': {
        'value': 'U2',
        'trend': '+',
    },
    'overall_assessment': {
        'value': 'U2',
        'trend': '+',
    },
    'report_observation': 'None',
}


SPECIES_MODEL_DATA = {
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

    'population_minimum_size': 1,
    'population_maximum_size': 12,
    'population_size_unit': 'i',
    'population_alt_minimum_size': 10,
    'population_alt_maximum_size': 120,
    'population_alt_size_unit': 'grids10x10',
    'population_method': '1',
    'population_trend': '-',
    'population_trend_period': '20082009',
    'population_trend_long': '+',
    'population_trend_long_period': '20102011',
    'complementary_favourable_population_op': '<',
    'complementary_favourable_population': 234,
    'complementary_favourable_population_method': 'foo pop method',
    'conclusion_population': 'U2',
    'conclusion_population_trend': '-',

    'habitat_surface_area': 100,
    'habitat_date': '2000-2001',
    'habitat_method': '3',
    'habitat_quality': '2',
    'habitat_quality_explanation': 'foo explanation',
    'habitat_trend': '0',
    'habitat_trend_period': '20042005',
    'habitat_trend_long': '0',
    'habitat_trend_long_period': '20062007',
    'habitat_area_suitable': 1000,
    'conclusion_habitat': 'U1',
    'conclusion_habitat_trend': '-',

    'conclusion_future': 'U2',
    'conclusion_future_trend': '+',

    'conclusion_assessment': 'U2',
    'conclusion_assessment_trend': '+',

    'cons_report_observation': 'None',
}


def _create_species_record(species_app, comment=False):
    from art17 import models
    with species_app.app_context():
        species = models.DataSpecies(id=1, code='1234')
        species.lu = models.LuHdSpecies(objectid=1, code=1234)
        record = models.DataSpeciesRegion(
            id=1,
            species=species,
            cons_role='assessment',
            region='ALP',
        )
        record.lu = models.LuBiogeoreg(objectid=1)
        models.db.session.add(record)

        if comment:
            comment = models.DataSpeciesRegion(
                id=2,
                species_id=1,
                cons_role='comment',
                region='ALP',
                range_surface_area=1337,
            )
            models.db.session.add(comment)

        models.db.session.commit()


def test_load_comments_view(species_app):
    _create_species_record(species_app)
    client = species_app.test_client()
    resp = client.get('/specii/detalii/1/comentarii')
    assert resp.status_code == 200


def test_save_comment_record(species_app):
    from art17.models import DataSpeciesRegion
    species_app.config['TESTING_USER_ID'] = 'smith'
    _create_species_record(species_app)
    client = species_app.test_client()
    resp = client.post('/specii/detalii/1/comentarii',
                       data={'range.surface_area': '50',
                             'range.method': '1',
                             'population.method': '1',
                             'habitat.surface_area': '100',
                             'habitat.date': '2000-2001',
                             'habitat.method': '1',
                             'habitat.quality': '2',
                             'habitat.quality_explanation': 'foo explanation',
                             'habitat.area_suitable': 1000})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        comment = DataSpeciesRegion.query.get(2)
        assert comment.cons_role == 'comment'
        assert comment.cons_user_id == 'smith'
        assert comment.species.code == '1234'
        assert comment.region == 'ALP'
        assert comment.range_surface_area == 50


def test_edit_comment_form(species_app):
    from art17.models import DataSpeciesRegion
    _create_species_record(species_app, comment=True)
    client = species_app.test_client()
    resp1 = client.get('/specii/comentarii/f3b4c23bcb88')
    assert resp1.status_code == 404
    resp2 = client.get('/specii/comentarii/2')
    assert resp2.status_code == 200
    assert '1337' in resp2.data


def test_edit_comment_submit(species_app):
    from art17.models import DataSpeciesRegion
    _create_species_record(species_app, comment=True)
    client = species_app.test_client()
    resp = client.post('/specii/comentarii/2',
                       data={'range.surface_area': '50',
                             'range.method': '1',
                             'population.method': '1',
                             'habitat.surface_area': '100',
                             'habitat.date': '2000-2001',
                             'habitat.method': '1',
                             'habitat.quality': '2',
                             'habitat.quality_explanation': 'foo explanation',
                             'habitat.area_suitable': 1000})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        comment = DataSpeciesRegion.query.get(2)
        assert comment.range_surface_area == 50


def test_one_field_required():
    from werkzeug.datastructures import MultiDict
    from art17 import forms
    form = forms.SpeciesComment(MultiDict())
    assert not form.validate()


def test_save_all_form_fields():
    from art17 import forms
    from art17 import models
    from art17.common import flatten_dict
    from art17.schemas import flatten_species_commentform
    from werkzeug.datastructures import MultiDict

    form_data = MultiDict(flatten_dict(SPECIES_STRUCT_DATA))

    form = forms.SpeciesComment(form_data)
    assert form.validate()

    comment = models.DataSpeciesRegion()
    flatten_species_commentform(form.data, comment)

    for k, v in SPECIES_MODEL_DATA.items():
        assert getattr(comment, k) == v


def test_flatten():
    from art17.schemas import flatten_species_commentform
    from art17 import models
    obj = models.DataSpeciesRegion()
    flatten_species_commentform(SPECIES_STRUCT_DATA, obj)
    for k, v in SPECIES_MODEL_DATA.items():
        assert getattr(obj, k) == v


def test_parse():
    from art17.schemas import parse_species_commentform
    from art17 import models
    obj = models.DataSpeciesRegion(**SPECIES_MODEL_DATA)
    data = parse_species_commentform(obj)
    assert data == SPECIES_STRUCT_DATA


def test_add_comment_reply(species_app):
    import flask
    from webtest import TestApp
    from art17.replies import replies
    from art17 import models
    from art17.common import common

    species_app.config['TESTING_USER_ID'] = 'somewho'
    _create_species_record(species_app, comment=True)
    species_app.register_blueprint(replies)
    species_app.register_blueprint(common)
    client = TestApp(species_app)
    page = client.get('/replici/specii/2')
    form = page.forms['reply-form']
    form['text'] = "hello world!"
    form.submit()

    with species_app.app_context():
        replies = models.CommentReply.query.all()
        assert len(replies) == 1
        msg = replies[0]
        assert msg.text == "hello world!"
        assert msg.user_id == 'somewho'
        assert msg.parent_table == 'species'
        assert msg.parent_id == '2'
