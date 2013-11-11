import pytest
from art17 import models
from test_species import _create_species_record


def _create_user_record(app):
    with app.app_context():
        user = models.NotificationUser(id=1, email='alex@test.ro', full_name='Prenume Nume')
        models.db.session.add(user)
        models.db.session.commit()


def test_add_species_region_comment(notifications_app):
    _create_species_record(notifications_app, comment=True)
    _create_user_record(notifications_app)
    client = notifications_app.test_client()
    resp = client.post('/specii/detalii/2/comentarii',
                       data={'range.surface_area': '50',
                             'range.method': '1',
                             'population.method': '1',
                             'habitat.surface_area': '100',
                             'habitat.date': '2000-2001',
                             'habitat.method': '1',
                             'habitat.quality': '2',
                             'habitat.quality_explanation': 'foo explanation',
                             'habitat.area_suitable': 1000})
    assert resp.status_code == 200