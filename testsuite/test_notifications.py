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
                            data=params.comment_data)
        assert resp.status_code == 200
        assert len(outbox) == 1
        assert 'user@example.com' in outbox[0].recipients
