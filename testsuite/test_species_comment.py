# encoding: utf-8

import pytest

COMMENT_SAVED_TXT = "Comentariul a fost înregistrat"


@pytest.fixture
def species_app():
    import flask
    from art17.species import species
    app = flask.Flask('art17.app')
    app.config['TESTING'] = True
    app.register_blueprint(species)
    from art17 import models as _models
    app.extensions['art17_models'] = _models
    _models.db.init_app(app)
    with app.app_context():
        _models.db.create_all()
    return app


def _create_species_record(species_app):
    from art17.app import models
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
    from art17.app import models
    _create_species_record(species_app)
    client = species_app.test_client()
    resp = client.post('/specii/detalii/1/comentariu',
                       data={'range_surface_area': '50'})
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with species_app.app_context():
        assert models.DataSpeciesComment.query.count() == 1
        comment = models.DataSpeciesComment.query.first()
        assert comment.range_surface_area == 50
