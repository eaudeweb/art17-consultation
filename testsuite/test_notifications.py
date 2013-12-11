# coding=utf-8
from contextlib import contextmanager
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
        cls.record = _create_species_record(app, comment)
        _create_user_record(app)


class notif_habitat_params(habitat_params):
    @classmethod
    def setup(cls, app, comment=False):
        from test_habitat import _create_habitat_record

        app.register_blueprint(habitat.habitat)
        app.register_blueprint(notifications.notifications)
        cls.record = _create_habitat_record(app, comment)
        _create_user_record(app)


class FakeLdap(object):

    def get_emails_for_group(self, group):
        return [self.get_user_info('smith')]

    def get_user_info(self, user_id):
        if user_id == 'smith':
            return {'email': 'user@example.com'}
        return {'email': 'unknown@exmaple.com', 'full_name': user_id}


@contextmanager
def _fake_ldap_open():
    yield FakeLdap()


@contextmanager
def ldap_patch():
    from art17 import ldap_access
    orig = ldap_access.__dict__['open_ldap_server']
    ldap_access.__dict__['open_ldap_server'] = _fake_ldap_open
    reload(notifications)
    try:
        yield
    finally:
        ldap_access.__dict__['open_ldap_server'] = orig
        reload(notifications)
    

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
        with ldap_patch():
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
        with ldap_patch():
            resp = client.post(params.comment_edit_url, data=params.comment_data,
                               follow_redirects=True)
            assert resp.status_code == 200
            assert len(outbox) == 0


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_update_status(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    with mail.record_messages() as outbox:
        with ldap_patch():
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
        with ldap_patch():
            resp = client.post(params.comment_delete_url, data={'next': '/'})
            assert resp.status_code == 302
            assert len(outbox) == 0


def test_reply_add(notifications_app):
    from art17 import replies
    notifications_app.register_blueprint(replies.replies)
    params = notif_species_params
    params.setup(notifications_app, comment=True)
    client = notifications_app.test_client()
    with mail.record_messages() as outbox:
        with ldap_patch():
            with notifications_app.test_request_context():
                resp = client.get('/_fake_login/smith')
                assert resp.status_code == 302
                resp = client.post('/replici/specii/%s/nou' % params.comment_id,
                                   data={'text': "hello world"})
                assert resp.status_code == 302
                assert len(outbox) == 0

                resp = client.get('/_fake_login/other_smith')
                assert resp.status_code == 302
                resp = client.post('/replici/specii/%s/nou' % params.comment_id,
                                    data={'text': "hello world from other"})
                assert resp.status_code == 302
                assert len(outbox) == 1


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_submit_for_evaluation(params, notifications_app):
    params.setup(notifications_app, comment=True)
    client = notifications_app.test_client()

    with mail.record_messages() as outbox:
        with ldap_patch():
            with notifications_app.test_request_context():
                comment = params.record
                comment.cons_role = 'comment-draft'
                comment.cons_user_id = 'smith2'
                models.db.session.add(comment)
                models.db.session.commit()
                resp = client.get('/_fake_login/smith2')
                assert resp.status_code == 302

                data = dict(params.comment_data)
                data['submit'] = 'evaluation'
                resp = client.post(params.comment_edit_url, data=data,
                                   follow_redirects=True)
                assert resp.status_code == 200
                assert len(outbox) == 1
                assert 'user@example.com' in outbox[0].recipients


@pytest.mark.parametrize(['params'], [[notif_species_params], [notif_habitat_params]])
def test_comment_final(params, app):
    params.setup(app, comment=True)
    client = app.test_client()

    with mail.record_messages() as outbox:
        with ldap_patch():
            orig = params.form_cls.final_validate
            params.form_cls.final_validate = lambda self: True
            resp = client.post(params.comment_finalize_url,
                               data={'next': params.comment_edit_url},
                               follow_redirects=True,
            )
            params.form_cls.final_validate = orig
            assert resp.status_code == 200
            assert len(outbox) == 1
            assert 'user@example.com' in outbox[0].recipients
            assert u'închisă' in outbox[0].body
