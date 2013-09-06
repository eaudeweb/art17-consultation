# encoding: utf-8

import pytest

COMMENT_SAVED_TXT = "Comentariul a fost înregistrat"
MISSING_FIELD_TXT = "Suprafața este obligatorie"


@pytest.fixture
def species_app():
    import flask
    from art17.species import species
    app = flask.Flask('art17.app')
    app.config['TESTING'] = True
    app.register_blueprint(species)
    from art17.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def _create_species_record(species_app):
    from art17 import models
    with species_app.app_context():
        species = models.DataSpecies(species_id=1, speciescode='1234')
        species.lu = models.LuHdSpecies(objectid=1, speciescode=1234)
        record = models.DataSpeciesRegion(sr_id=1, sr_species=species)
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


def test_save_all_form_fields():
    from art17 import species_forms
    from art17 import models
    from werkzeug.datastructures import MultiDict

    form_data = MultiDict({
        'range.surface_area': '123',
        'range.method': 'foo range method',
        'range.trend_short.trend': 'foo range trend short',
        'range.trend_short.period_min': 'foomin',
        'range.trend_short.period_max': 'foomax',
        'range.trend_long.trend': 'bar range trend long',
        'range.trend_long.period_min': 'barmin',
        'range.trend_long.period_max': 'barmax',
        'range.reference_value.op': 'foo op',
        'range.reference_value.number': '456',
        'range.favourable_method': 'foo method',
        'range.conclusion.value': 'U1',
        'range.conclusion.trend': 'foo conclusion trend',
    })

    form = species_forms.SpeciesComment(form_data)
    comment = models.DataSpeciesComment()
    form.populate_obj(comment)

    assert comment.range_surface_area == 123
    assert comment.range_method == 'foo range method'
    assert comment.range_trend == 'foo range trend short'
    assert comment.range_trend_period == 'foomin-foomax'
    assert comment.range_trend_long == 'bar range trend long'
    assert comment.range_trend_long_period == 'barmin-barmax'
    assert comment.complementary_favourable_range_op == 'foo op'
    assert comment.complementary_favourable_range == 456
    assert comment.complementary_favourable_range_method == 'foo method'
    assert comment.conclusion_range == 'U1'
    assert comment.conclusion_range_trend == 'foo conclusion trend'
