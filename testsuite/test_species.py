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
            'magnitude': {
                'min': None,
                'max': None,
            },
        },
        'trend_long': {
            'trend': '-',
            'period': {
                'start': '2002',
                'end': '2003',
            },
            'magnitude': {
                'min': None,
                'max': None,
            },
        },
        'reference_value': {
            'method': 'foo method',
            'number': 456,
            'op': '>',
            'x': None,
        },
        'reason': {},
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
        'additional_locality': None,
        'additional_method': None,
        'additional_problems': None,
        'date': '2010',
        'method': '1',
        'trend_short': {
            'trend': '-',
            'period': {
                'start': '2008',
                'end': '2009',
            },
            'method': '1',
            'magnitude': {
                'min': None,
                'max': None,
                'ci': None,
            },
        },
        'trend_long': {
            'trend': '+',
            'period': {
                'start': '2010',
                'end': '2011',
            },
            'method': '1',
            'magnitude': {
                'min': None,
                'max': None,
                'ci': None,
            },
        },
        'reference_value': {
            'method': 'foo pop method',
            'number': 234,
            'op': '<',
            'x': None,
        },
        'reason': {},
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
    'pressures': {
        'pressures_method': '1'
    },
    'threats': {
        'threats_method': '1'
    },
    'measures': {
    },
    'infocomp': {
        'justification': '-',
        'other_relevant_information': '--',
        'transboundary_assessment': '---',
    },
    'natura2000': {
        'population': {
            'min': 2,
            'max': 6,
            'unit': '',
        },
        'method': '',
        'trend': '',
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
    'generalstatus': '1',

    'published': 'someday',
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
    'population_date': '2010',
    'population_method': '1',
    'population_trend': '-',
    'population_trend_period': '20082009',
    'population_trend_method': '1',
    'population_trend_long': '+',
    'population_trend_long_period': '20102011',
    'population_trend_long_method': '1',
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
    'pressures_method': '1',
    'threats_method': '1',
    'justification': '-',
    'other_relevant_information': '--',
    'transboundary_assessment': '---',
    'natura2000_population_min': 2,
    'natura2000_population_max': 6,
    'natura2000_population_unit': '',
    'natura2000_population_method': '',
    'natura2000_population_trend': '',
    'conclusion_habitat': 'U1',
    'conclusion_habitat_trend': '-',

    'conclusion_future': 'U2',
    'conclusion_future_trend': '+',

    'conclusion_assessment': 'U2',
    'conclusion_assessment_trend': '+',

    'cons_report_observation': 'nothing to add',
    'cons_generalstatus': '1',

    'published': 'someday',
}


def _create_species_record(species_app, comment=False):
    from art17 import models
    with species_app.app_context():
        species = models.DataSpecies(id=1, code='1234')
        species.lu = models.LuHdSpecies(objectid=1, code=1234, group_code='M')
        record = models.DataSpeciesRegion(
            id=1,
            species=species,
            cons_role='assessment',
            region='ALP',
            cons_dataset_id=1,
        )
        record.lu = models.LuBiogeoreg(objectid=1)
        models.db.session.add(record)


        if comment:
            comment = models.DataSpeciesRegion(
                id=2,
                species_id=1,
                cons_role='comment',
                cons_user_id='smith',
                cons_dataset_id=1,
                region='ALP',
                range_surface_area=1337,
            )
            models.db.session.add(comment)

        models.db.session.commit()
        return comment or record


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
                             'habitat.area_suitable': 1000},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        comment = DataSpeciesRegion.query.get(2)
        assert comment.cons_role == 'comment-draft'
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
                             'habitat.area_suitable': 1000},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        comment = DataSpeciesRegion.query.get(2)
        assert comment.range_surface_area == 50


def test_extra_fields_save(species_app):
    import json
    from art17.models import DataSpeciesRegion, LuThreats, LuRanking, LuPollution
    from art17 import models
    species_app.config['TESTING_USER_ID'] = 'smith'
    _create_species_record(species_app)
    with species_app.app_context():
        pressure = LuThreats(code='1')
        ranking = LuRanking(code='M')
        pollution = LuPollution(code='A')
        models.db.session.add(pressure)
        models.db.session.add(ranking)
        models.db.session.add(pollution)
        models.db.session.commit()
    pressure_data = json.dumps({'pressure': '1', 'ranking': 'M', 'pollutions': ['A']})
    measure_data = json.dumps({'measurecode': '1', 'rankingcode': 'M'})
    client = species_app.test_client()
    resp = client.post('/specii/detalii/1/comentarii',
                       data={'pressures.pressures': [pressure_data],
                             'measures.measures': [measure_data]},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        comment = DataSpeciesRegion.query.get(2)
        assert comment.cons_role == 'comment-draft'
        assert comment.cons_user_id == 'smith'
        assert len(list(comment.pressures)) == 1
        assert comment.pressures[0].pressure == '1'
        assert comment.pressures[0].ranking == 'M'
        assert comment.pressures[0].pollutions[0].pollution_qualifier == 'A'
        assert comment.measures[0].measurecode == '1'


def test_one_field_required(species_app):
    from werkzeug.datastructures import MultiDict
    from art17 import forms
    with species_app.app_context():
        form = forms.SpeciesComment(MultiDict())
        assert not form.validate()


def test_save_all_form_fields(species_app):
    from art17 import forms
    from art17 import models
    from art17.common import flatten_dict
    from art17.schemas import flatten_species_commentform
    from werkzeug.datastructures import MultiDict

    form_data = MultiDict(flatten_dict(SPECIES_STRUCT_DATA))

    with species_app.app_context():
        form = forms.SpeciesComment(form_data)
        form.validate()
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


def test_save_taxonomic_reserve_comment(species_app):
    from art17.models import DataSpeciesRegion
    #species_app.config['TESTING_USER_ID'] = 'smith'
    _create_species_record(species_app)
    client = species_app.test_client()
    resp = client.post(
        '/specii/detalii/1/comentarii',
        data={'generalstatus': 'SR TAX'},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        comment = DataSpeciesRegion.query.get(2)
        assert comment.cons_generalstatus == 'SR TAX'


def test_permissions(species_app):
    from art17 import models, common
    from flask.ext.principal import RoleNeed, UserNeed
    _create_species_record(species_app, comment=True)

    with species_app.app_context():
        row = models.DataSpeciesRegion.query.get(1)
        comment = models.DataSpeciesRegion.query.get(2)

        assert common.perm_create_comment(row).needs == set([
            RoleNeed('admin'),
            RoleNeed('expert'),
            RoleNeed('expert:species'),
            RoleNeed('expert:species:M'),
            RoleNeed('expert:species:M:1234'),
        ])

        assert common.perm_edit_comment(comment).needs == set([
            RoleNeed('admin'),
            UserNeed('smith'),
        ])

        assert common.perm_update_comment_status(comment).needs == set([
            RoleNeed('admin'),
            RoleNeed('reviewer'),
            RoleNeed('reviewer:species'),
            RoleNeed('reviewer:species:M'),
            RoleNeed('reviewer:species:M:1234'),
        ])

        assert common.perm_delete_comment(comment).needs == set([
            RoleNeed('admin'),
            UserNeed('smith'),
        ])
