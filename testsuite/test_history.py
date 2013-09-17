def test_species_comment_add(app):
    from art17 import models, species, history
    from test_species_comment import _create_species_record
    app.register_blueprint(species.species)
    app.register_blueprint(history.history)
    _create_species_record(app)
    user_id = app.config['TESTING_USER_ID'] = 'somebody'
    client = app.test_client()

    resp = client.post('/specii/detalii/1/comentariu',
                       data={'range.surface_area': '50', 'range.method': '1'})
    assert resp.status_code == 200

    with app.app_context():
        history = models.History.query.all()
        comment = models.DataSpeciesComment.query.first()
        assert len(history) == 1
        assert history[0].table == 'data_species_comments'
        assert history[0].object_id == comment.id
        assert history[0].action == 'add'
        assert history[0].user_id == user_id



def test_habitat_comment_add(app):
    from art17 import models, habitat, history
    from test_habitat_comment import _create_habitat_record
    app.register_blueprint(habitat.habitat)
    app.register_blueprint(history.history)
    _create_habitat_record(app)
    user_id = app.config['TESTING_USER_ID'] = 'somebody'
    client = app.test_client()

    resp = client.post('/habitate/detalii/1/comentariu',
                       data={'range.surface_area': '50', 'range.method': '1'})
    assert resp.status_code == 200

    with app.app_context():
        history = models.History.query.all()
        comment = models.DataHabitattypeComment.query.first()
        assert len(history) == 1
        assert history[0].table == 'data_habitattype_comments'
        assert history[0].object_id == comment.id
        assert history[0].action == 'add'
        assert history[0].user_id == user_id
