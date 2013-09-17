import pytest
from art17 import models, species, habitat, history


class species_params(object):
    blueprint = species.species
    comment_table = 'data_species_comments'
    comment_create_url = '/specii/detalii/1/comentariu'
    user_id = 'somebody'
    comment_cls = models.DataSpeciesComment

    @classmethod
    def setup(cls, app):
        from test_species_comment import _create_species_record
        app.register_blueprint(species.species)
        app.register_blueprint(history.history)
        _create_species_record(app)
        app.config['TESTING_USER_ID'] = cls.user_id


class habitat_params(object):
    blueprint = habitat.habitat
    comment_table = 'data_habitattype_comments'
    comment_create_url = '/habitate/detalii/1/comentariu'
    user_id = 'somebody'
    comment_cls = models.DataHabitattypeComment

    @classmethod
    def setup(cls, app):
        from test_habitat_comment import _create_habitat_record
        app.register_blueprint(habitat.habitat)
        app.register_blueprint(history.history)
        _create_habitat_record(app)
        app.config['TESTING_USER_ID'] = cls.user_id


@pytest.mark.parametrize(['spec'], [[species_params], [habitat_params]])
def test_comment_add(spec, app):
    spec.setup(app)
    client = app.test_client()

    resp = client.post(spec.comment_create_url,
                       data={'range.surface_area': '50', 'range.method': '1'})
    assert resp.status_code == 200

    with app.app_context():
        history = models.History.query.all()
        comment = spec.comment_cls.query.first()
        assert len(history) == 1
        assert history[0].table == spec.comment_table
        assert history[0].object_id == comment.id
        assert history[0].action == 'add'
        assert history[0].user_id == spec.user_id
