import pytest


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
