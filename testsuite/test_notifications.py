import pytest
from art17 import models
from art17.notifications import mail
from test_species import _create_species_record


def _create_user_record(app):
    with app.app_context():
        user = models.NotificationUser(id=1, email='user@example.com', full_name='Prenume Nume')
        models.db.session.add(user)
        models.db.session.commit()


def test_add_species_region_comment(notifications_app):
    _create_species_record(notifications_app, comment=True)
    _create_user_record(notifications_app)
    client = notifications_app.test_client()
    with mail.record_messages() as outbox:
        resp = client.post('/specii/detalii/2/comentarii',
                       data={'range.surface_area': '50'})
        assert resp.status_code == 200
        assert len(outbox) == 1
        assert 'user@example.com' in outbox[0].recipients
