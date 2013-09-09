# encoding: utf-8

import pytest

COMMENT_SAVED_TXT = "Comentariul a fost înregistrat"


@pytest.fixture
def habitat_app():
    import flask
    from art17.habitat import habitat
    app = flask.Flask('art17.app')
    app.config['TESTING'] = True
    app.register_blueprint(habitat)
    from art17.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


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
