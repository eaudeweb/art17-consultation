import pytest
from art17 import models
from art17 import species
from art17 import habitat
from art17 import notifications
from art17.notifications import mail
from test_history import species_params, habitat_params


class notif_species_params(species_params):
    @classmethod
    def setup(cls, app, comment=False):
        from test_species import _create_species_record

        app.register_blueprint(species.species)
        app.register_blueprint(notifications.notifications)
        _create_species_record(app, comment)
        _create_user_record(app)


class notif_habitat_params(habitat_params):
    @classmethod
    def setup(cls, app, comment=False):
        from test_habitat import _create_habitat_record

        app.register_blueprint(habitat.habitat)
        app.register_blueprint(notifications.notifications)
        _create_habitat_record(app, comment)
        _create_user_record(app)


def _create_user_record(app):
    with app.app_context():
        user = models.NotificationUser(id=1, email='user@example.com', full_name='Prenume Nume')
        models.db.session.add(user)
        models.db.session.commit()


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_add(params, app):
    params.setup(app)
    client = app.test_client()

    with mail.record_messages() as outbox:
        resp = client.post(params.comment_create_url,
                           data=params.comment_data,
                           follow_redirects=True)
        assert resp.status_code == 200
        assert len(outbox) == 1
        assert 'user@example.com' in outbox[0].recipients


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_edit(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    with mail.record_messages() as outbox:
        resp = client.post(params.comment_edit_url, data=params.comment_data,
                           follow_redirects=True)
        assert resp.status_code == 200
        assert len(outbox) == 1
        assert 'user@example.com' in outbox[0].recipients


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_update_status(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    with mail.record_messages() as outbox:
        resp = client.post(params.comment_status_url,
                           data={'status': 'approved', 'next': '/'}
        )
        assert resp.status_code == 302
        assert len(outbox) == 1
        assert 'user@example.com' in outbox[0].recipients


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_delete(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    with mail.record_messages() as outbox:
        resp = client.post(params.comment_delete_url, data={'next': '/'})
        assert resp.status_code == 302
        assert len(outbox) == 1
        assert 'user@example.com' in outbox[0].recipients


def test_reply_add(app):
    from art17 import replies
    params = notif_species_params
    app.register_blueprint(replies.replies)
    params.setup(app, comment=True)
    client = app.test_client()
    with mail.record_messages() as outbox:
        resp = client.post('/replici/specii/%s/nou' % params.comment_id,
                           data={'text': "hello world"})
        assert resp.status_code == 302
        assert len(outbox) == 1


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_submit_for_evaluation(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    with mail.record_messages() as outbox:
        data = dict(params.comment_data)
        data['submit'] = 'evaluation'
        resp = client.post(params.comment_edit_url, data=data,
                           follow_redirects=True)
        assert resp.status_code == 200
        assert len(outbox) == 2
        assert 'user@example.com' in outbox[0].recipients
        assert 'user@example.com' in outbox[1].recipients
        assert 'evaluare' in outbox[1].body



@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_final(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    with mail.record_messages() as outbox:
        print params.comment_finalize_url
        resp = client.post(params.comment_finalize_url, data={'next': '/'})
        print resp.data
        assert resp.status_code == 302
        assert len(outbox) == 1
        assert 'user@example.com' in outbox[0].recipients
        assert 'final' in outbox[0].body
