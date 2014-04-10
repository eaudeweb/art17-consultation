# coding=utf-8
import flask
from flask.ext.principal import PermissionDenied
from mock import Mock
from art17.auth import need
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
        assert comment.cons_role == 'final-draft'
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
        assert comment.cons_role == 'final-draft'
        assert comment.range_surface_area == 42


def test_role_and_status_modified(aggregation_app):
    from art17.models import DataSpeciesRegion
    from art17.forms import SpeciesComment
    _create_species_record(aggregation_app)
    client = aggregation_app.test_client()

    with aggregation_app.app_context():
        species = DataSpeciesRegion.query.get(1)
        assert species.cons_role == 'assessment'

    resp = client.post('/dataset/1/specii/1/',
                       data={'range.surface_area': '42'},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with aggregation_app.app_context():
        comment = DataSpeciesRegion.query.get(1)
        assert comment.cons_role == 'final-draft'
        assert comment.cons_status == 'new'

    original_final = SpeciesComment.final_validate
    SpeciesComment.final_validate = lambda self: True
    resp = client.get('/dataset/1/specii/1/finalize')
    SpeciesComment.final_validate = original_final

    assert resp.status_code == 302
    with aggregation_app.app_context():
        comment = DataSpeciesRegion.query.get(1)
        assert comment.cons_role == 'final'
        assert comment.cons_status == 'finalized'


def test_role_and_status_unmodified(aggregation_app):
    from art17.models import DataSpeciesRegion
    from art17.forms import SpeciesComment
    _create_species_record(aggregation_app)
    client = aggregation_app.test_client()

    with aggregation_app.app_context():
        species = DataSpeciesRegion.query.get(1)
        assert species.cons_role == 'assessment'
        assert species.cons_status == 'new'

    original_final = SpeciesComment.final_validate
    SpeciesComment.final_validate = lambda self: True
    resp = client.get('/dataset/1/specii/1/finalize')
    SpeciesComment.final_validate = original_final
    assert resp.status_code == 302
    with aggregation_app.app_context():
        comment = DataSpeciesRegion.query.get(1)
        assert comment.cons_role == 'final'
        assert comment.cons_status == 'unmodified'


def test_role_and_status_definalize_unmodified(aggregation_app):
    from art17.models import DataSpeciesRegion
    from art17.forms import SpeciesComment
    _create_species_record(aggregation_app)
    client = aggregation_app.test_client()

    with aggregation_app.app_context():
        species = DataSpeciesRegion.query.get(1)
        assert species.cons_role == 'assessment'
        assert species.cons_status == 'new'

    original_final = SpeciesComment.final_validate
    SpeciesComment.final_validate = lambda self: True
    resp = client.get('/dataset/1/specii/1/finalize')
    SpeciesComment.final_validate = original_final
    assert resp.status_code == 302

    resp = client.get('/dataset/1/specii/1/definalize')
    assert resp.status_code == 302
    with aggregation_app.app_context():
        comment = DataSpeciesRegion.query.get(1)
        assert comment.cons_role == 'assessment'
        assert comment.cons_status == 'new'


def test_role_and_status_definalize_modified(aggregation_app):
    from art17.models import DataSpeciesRegion
    _create_species_record(aggregation_app)
    client = aggregation_app.test_client()

    with aggregation_app.app_context():
        species = DataSpeciesRegion.query.get(1)
        assert species.cons_role == 'assessment'

    resp = client.post('/dataset/1/specii/1/',
                       data={'range.surface_area': '42'},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data

    resp = client.get('/dataset/1/specii/1/finalize')
    assert resp.status_code == 302

    resp = client.get('/dataset/1/specii/1/definalize')
    assert resp.status_code == 302
    with aggregation_app.app_context():
        comment = DataSpeciesRegion.query.get(1)
        assert comment.cons_role == 'final-draft'
        assert comment.cons_status == 'new'


def test_history_habitat_update(aggregation_app):
    from art17.models import DataHabitattypeRegion, History
    _create_habitat_record(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.post('/dataset/1/habitate/1/',
                       data={'range.surface_area': '42'},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert COMMENT_SAVED_TXT in resp.data
    with aggregation_app.app_context():
        comment = DataHabitattypeRegion.query.get(1)
        assert comment.cons_role == 'final-draft'
        assert comment.range_surface_area == 42

        history = History.query.all()
        assert history[0].table == 'data_habitattype_regions'
        assert history[0].action == 'edit'
        assert history[0].object_id == str(comment.id)
        assert history[0].dataset_id == comment.cons_dataset_id


def test_aggregation_roles(aggregation_app):
    client = aggregation_app.test_client()
    try:
        client.get('/executa_agregare')
    except PermissionDenied:
        pass

    @aggregation_app.before_request
    def set_identity():
        flask.g.identity = Mock(id='bar', provides=[need.admin])

    resp = client.get('/executa_agregare')
    assert resp.status_code == 200
