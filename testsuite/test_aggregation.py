# coding=utf-8
from test_habitat import _create_habitat_record
from test_species import _create_species_record


COMMENT_SAVED_TXT = "Înregistrarea a fost actualizată"


def test_update_habitat_record(aggregation_app):
    from art17.models import DataHabitattypeRegion
    _create_habitat_record(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.post('/dataset/1/habitate/1/',
                       data={'range.surface_area': '42'},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with aggregation_app.app_context():
        comment = DataHabitattypeRegion.query.get(1)
        assert comment.cons_role == 'assessment'
        assert comment.range_surface_area == 42


def test_update_species_record(aggregation_app):
    from art17.models import DataSpeciesRegion
    _create_species_record(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.post('/dataset/1/specii/1/',
                       data={'range.surface_area': '42'},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with aggregation_app.app_context():
        comment = DataSpeciesRegion.query.get(1)
        assert comment.cons_role == 'assessment'
        assert comment.range_surface_area == 42
