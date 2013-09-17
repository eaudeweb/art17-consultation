from datetime import datetime
import pytest
from flask import json
from art17 import models, species, habitat, history


class species_params(object):
    blueprint = species.species
    comment_table = 'data_species_comments'
    comment_create_url = '/specii/detalii/1/comentariu'
    user_id = 'somebody'
    comment_cls = models.DataSpeciesComment
    comment_id = '4f799fdd6f5a'
    comment_edit_url = '/specii/comentariu/4f799fdd6f5a'
    comment_status_url = '/specii/comentariu/4f799fdd6f5a/stare'
    comment_data = {'range.surface_area': '50',
                    'range.method': '1',
                    'population.method': '1',
                    'habitat.surface_area': '100',
                    'habitat.date': '2000-2001',
                    'habitat.method': '1',
                    'habitat.quality': '2',
                    'habitat.quality_explanation': 'foo explanation',
                    'habitat.area_suitable': 1000}

    @classmethod
    def setup(cls, app, comment=False):
        from test_species_comment import _create_species_record
        app.register_blueprint(species.species)
        app.register_blueprint(history.history)
        _create_species_record(app, comment)
        app.config['TESTING_USER_ID'] = cls.user_id


class habitat_params(object):
    blueprint = habitat.habitat
    comment_table = 'data_habitattype_comments'
    comment_create_url = '/habitate/detalii/1/comentariu'
    user_id = 'somebody'
    comment_cls = models.DataHabitattypeComment
    comment_id = '4f799fdd6f5a'
    comment_edit_url = '/habitate/comentariu/4f799fdd6f5a'
    comment_status_url = '/habitate/comentariu/4f799fdd6f5a/stare'
    comment_data = {'range.surface_area': '50',
                    'range.method': '1'}

    @classmethod
    def setup(cls, app, comment=False):
        from test_habitat_comment import _create_habitat_record
        app.register_blueprint(habitat.habitat)
        app.register_blueprint(history.history)
        _create_habitat_record(app, comment)
        app.config['TESTING_USER_ID'] = cls.user_id


@pytest.mark.parametrize(['params'], [[species_params], [habitat_params]])
def test_comment_add(params, app):
    params.setup(app)
    client = app.test_client()

    resp = client.post(params.comment_create_url, data=params.comment_data)
    assert resp.status_code == 200

    with app.app_context():
        history = models.History.query.all()
        comment = params.comment_cls.query.first()
        assert len(history) == 1
        assert history[0].table == params.comment_table
        assert history[0].object_id == comment.id
        assert history[0].action == 'add'
        assert history[0].user_id == params.user_id
        assert json.loads(history[0].new_data)['range']['surface_area'] == 50


@pytest.mark.parametrize(['params'], [[species_params], [habitat_params]])
def test_comment_edit(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    resp = client.post(params.comment_edit_url, data=params.comment_data)
    assert resp.status_code == 200

    with app.app_context():
        history = models.History.query.all()
        comment = params.comment_cls.query.first()
        assert len(history) == 1
        assert history[0].table == params.comment_table
        assert history[0].object_id == comment.id
        assert history[0].action == 'edit'
        assert history[0].user_id == params.user_id
        assert json.loads(history[0].old_data)['range']['surface_area'] == 1337
        assert json.loads(history[0].new_data)['range']['surface_area'] == 50


@pytest.mark.parametrize(['params'], [[species_params], [habitat_params]])
def test_comment_update_status(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    resp = client.post(params.comment_status_url,
                       data={'status': 'approved', 'next': '/'})
    assert resp.status_code == 302

    with app.app_context():
        history = models.History.query.all()
        comment = params.comment_cls.query.first()
        assert len(history) == 1
        assert history[0].table == params.comment_table
        assert history[0].object_id == comment.id
        assert history[0].action == 'status'
        assert history[0].user_id == params.user_id
        assert json.loads(history[0].old_data) == 'new'
        assert json.loads(history[0].new_data) == 'approved'


def test_message_add(app):
    from art17 import messages
    params = species_params
    app.register_blueprint(messages.messages)
    params.setup(app, comment=True)
    client = app.test_client()
    resp = client.post('/mesaje/%s/nou' % params.comment_id,
                       data={'text': "hello world"})
    assert resp.status_code == 302

    with app.app_context():
        history = models.History.query.all()
        message = models.CommentMessage.query.first()
        assert len(history) == 1
        assert history[0].table == 'comment_messages'
        assert history[0].object_id == message.id
        assert history[0].action == 'add'
        assert history[0].user_id == params.user_id
        new_data = json.loads(history[0].new_data)
        assert new_data['text'] == 'hello world'
        assert new_data['user_id'] == params.user_id
        assert new_data['parent'] == params.comment_id


def test_message_remove(app):
    from art17 import messages
    user_id = app.config['TESTING_USER_ID'] = 'somebody'
    app.register_blueprint(history.history)
    app.register_blueprint(messages.messages)

    with app.app_context():
        message = models.CommentMessage(text='hello foo',
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
        assert history_items[0].table == 'comment_messages'
        assert history_items[0].object_id == message_id
        assert history_items[0].action == 'remove'
        assert history_items[0].user_id == user_id
        assert json.loads(history_items[0].old_data) == {
            'text': 'hello foo',
            'user_id': 'somewho',
            'parent': '123',
            'date': datetime(2010, 1, 4).isoformat(),
        }
