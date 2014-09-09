import flask
from art17 import models


def execute(query):
    app = flask.current_app
    aggregation_engine = models.db.get_engine(app, 'primary')
    return models.db.session.execute(query, bind=aggregation_engine)


def get_habitat_published(habcode, region):
    rv = []
    for row in execute(
        "SELECT autori, titlu_lucrare, an, publicatie, editura, oras, volum, pagini, "
        "FROM bibliografie b, "
             "fise_padurifise_padur_8916a21f fp, "
             "fise_paduri f "
        "WHERE fp.biblio=b.\"Oid\" "
        "AND fp.fise_paduri=f.\"Oid\" "
        "AND f.habitat_necorectat='{habcode}' "
        "AND f.reg_biogeg='{region}' ".format(habcode=habcode, region=region)
        ):
        rv.append(', '.join(row) + '\n')
    return ''.join(rv)
