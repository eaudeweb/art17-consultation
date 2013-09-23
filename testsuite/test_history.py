from datetime import datetime
import pytest
from flask import json
from art17 import models, species, habitat, history


class species_params(object):
    blueprint = species.species
    conclusion_table = 'data_species_conclusions'
    conclusion_create_url = '/specii/detalii/1/concluzii'
    user_id = 'somebody'
    conclusion_cls = models.DataSpeciesConclusion
    conclusion_id = '4f799fdd6f5a'
    conclusion_edit_url = '/specii/concluzii/4f799fdd6f5a'
    conclusion_status_url = '/specii/concluzii/4f799fdd6f5a/stare'
    conclusion_delete_url = '/specii/concluzii/4f799fdd6f5a/sterge'
    conclusion_data = {'range.surface_area': '50',
                       'range.method': '1',
                       'population.method': '1',
                       'habitat.surface_area': '100',
                       'habitat.date': '2000-2001',
                       'habitat.method': '1',
                       'habitat.quality': '2',
                       'habitat.quality_explanation': 'foo explanation',
                       'habitat.area_suitable': 1000}

    @classmethod
    def setup(cls, app, conclusion=False):
        from test_species_conclusion import _create_species_record
        app.register_blueprint(species.species)
        app.register_blueprint(history.history)
        _create_species_record(app, conclusion)
        app.config['TESTING_USER_ID'] = cls.user_id


class habitat_params(object):
    blueprint = habitat.habitat
    conclusion_table = 'data_habitattype_conclusions'
    conclusion_create_url = '/habitate/detalii/1/concluzii'
    user_id = 'somebody'
    conclusion_cls = models.DataHabitattypeConclusion
    conclusion_id = '4f799fdd6f5a'
    conclusion_edit_url = '/habitate/concluzii/4f799fdd6f5a'
    conclusion_status_url = '/habitate/concluzii/4f799fdd6f5a/stare'
    conclusion_delete_url = '/habitate/concluzii/4f799fdd6f5a/sterge'
    conclusion_data = {'range.surface_area': '50',
                       'range.method': '1',
                        'coverage.surface_area': 123,
                        'coverage.date': '2001',
                        'coverage.method': '1'}

    @classmethod
    def setup(cls, app, conclusion=False):
        from test_habitat_conclusion import _create_habitat_record
        app.register_blueprint(habitat.habitat)
        app.register_blueprint(history.history)
        _create_habitat_record(app, conclusion)
        app.config['TESTING_USER_ID'] = cls.user_id


@pytest.mark.parametrize(['params'], [[species_params], [habitat_params]])
def test_conclusion_add(params, app):
    params.setup(app)
    client = app.test_client()

    resp = client.post(params.conclusion_create_url,
                       data=params.conclusion_data)
    assert resp.status_code == 200

    with app.app_context():
        history = models.History.query.all()
        conclusion = params.conclusion_cls.query.first()
        assert len(history) == 1
        assert history[0].table == params.conclusion_table
        assert history[0].object_id == conclusion.id
        assert history[0].action == 'add'
        assert history[0].user_id == params.user_id
        assert json.loads(history[0].new_data)['range']['surface_area'] == 50


@pytest.mark.parametrize(['params'], [[species_params], [habitat_params]])
def test_conclusion_edit(params, app):
    params.setup(app, conclusion=True)
    client = app.test_client()

    resp = client.post(params.conclusion_edit_url, data=params.conclusion_data)
    assert resp.status_code == 200

    with app.app_context():
        history = models.History.query.all()
        conclusion = params.conclusion_cls.query.first()
        assert len(history) == 1
        assert history[0].table == params.conclusion_table
        assert history[0].object_id == conclusion.id
        assert history[0].action == 'edit'
        assert history[0].user_id == params.user_id
        assert json.loads(history[0].old_data)['range']['surface_area'] == 1337
        assert json.loads(history[0].new_data)['range']['surface_area'] == 50


@pytest.mark.parametrize(['params'], [[species_params], [habitat_params]])
def test_conclusion_update_status(params, app):
    params.setup(app, conclusion=True)
    client = app.test_client()

    resp = client.post(params.conclusion_status_url,
                       data={'status': 'approved', 'next': '/'})
    assert resp.status_code == 302

    with app.app_context():
        history = models.History.query.all()
        conclusion = params.conclusion_cls.query.first()
        assert len(history) == 1
        assert history[0].table == params.conclusion_table
        assert history[0].object_id == conclusion.id
        assert history[0].action == 'status'
        assert history[0].user_id == params.user_id
        assert json.loads(history[0].old_data) == 'new'
        assert json.loads(history[0].new_data) == 'approved'


@pytest.mark.parametrize(['params'], [[species_params], [habitat_params]])
def test_conclusion_delete(params, app):
    params.setup(app, conclusion=True)
    client = app.test_client()

    resp = client.post(params.conclusion_delete_url, data={'next': '/'})
    assert resp.status_code == 302

    with app.app_context():
        history = models.History.query.all()
        conclusion = params.conclusion_cls.query.first()
        assert len(history) == 1
        assert history[0].table == params.conclusion_table
        assert history[0].object_id == conclusion.id
        assert history[0].action == 'delete'
        assert history[0].user_id == params.user_id
        assert json.loads(history[0].old_data)['range']['surface_area'] == 1337
        assert json.loads(history[0].old_data)['_status'] == 'new'


def test_message_add(app):
    from art17 import messages
    params = species_params
    app.register_blueprint(messages.messages)
    params.setup(app, conclusion=True)
    client = app.test_client()
    resp = client.post('/mesaje/%s/nou' % params.conclusion_id,
                       data={'text': "hello world"})
    assert resp.status_code == 302

    with app.app_context():
        history = models.History.query.all()
        message = models.ConclusionMessage.query.first()
        assert len(history) == 1
        assert history[0].table == 'conclusion_messages'
        assert history[0].object_id == message.id
        assert history[0].action == 'add'
        assert history[0].user_id == params.user_id
        new_data = json.loads(history[0].new_data)
        assert new_data['text'] == 'hello world'
        assert new_data['user_id'] == params.user_id
        assert new_data['parent'] == params.conclusion_id


def test_message_remove(app):
    from art17 import messages
    user_id = app.config['TESTING_USER_ID'] = 'somebody'
    app.register_blueprint(history.history)
    app.register_blueprint(messages.messages)

    with app.app_context():
        message = models.ConclusionMessage(text='hello foo',
                                           user_id='somewho',
                                           parent='123',
                                           date=datetime(2010, 1, 4))
        models.db.session.add(message)
        models.db.session.commit()
        message_id = message.id

    client = app.test_client()
    resp = client.post('/mesaje/sterge?message_id=%s&next=/' % message_id)
    assert resp.status_code == 302

    with app.app_context():
        history_items = models.History.query.all()
        assert len(history_items) == 1
        assert history_items[0].table == 'conclusion_messages'
        assert history_items[0].object_id == message_id
        assert history_items[0].action == 'remove'
        assert history_items[0].user_id == user_id
        assert json.loads(history_items[0].old_data) == {
            'text': 'hello foo',
            'user_id': 'somewho',
            'parent': '123',
            'date': datetime(2010, 1, 4).isoformat(),
        }
