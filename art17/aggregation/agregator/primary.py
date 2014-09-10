import flask
from art17 import models


def execute(query):
    app = flask.current_app
    aggregation_engine = models.db.get_engine(app, 'primary')
    return models.db.session.execute(query, bind=aggregation_engine)


def get_habitat_published(habcode, region):
    rv = []
    for row in execute(
        "SELECT autori, titlu_lucrare, an, publicatie, editura, oras, volum, pagini "
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


def get_habitat_typical_species(habcode, region):
    rv = []
    for row in execute(
        "SELECT DISTINCT sa.\"Name\", count(fp.\"Oid\") as cnt "
        "FROM arboretspecii asp, fise_paduri fp, speciiarbori sa "
        "WHERE asp.fisa_pad=fp.\"Oid\" "
        "AND asp.species_id=sa.\"Code\" "
        "AND fp.habitat_necorectat='{habcode}' "
        "AND fp.reg_biogeg='{region}' "
        "GROUP BY sa.\"Name\" "
        "ORDER BY cnt DESC".format(habcode=habcode, region=region)
        ):
        rv.append(row[0])
    return rv


def get_pressures_threats(habcode, region):
    type_map = {
        None: None,  # ???
        1: 't',  # threat
        2: 'p',  # pressure
    }

    rv = []
    for row in execute(
        "SELECT tip, amenintari, rang, poluare "
        "FROM amenintari_pad a, "
             "fise_paduri fp "
        "WHERE a.fise_paduri=fp.\"Oid\" "
        #"AND a.tip=1 "
        "AND fp.habitat_necorectat='{habcode}' "
        "AND fp.reg_biogeg='{region}' ".format(habcode=habcode, region=region)
        ):
        rv.append({
            'pressure': row.amenintari,
            'ranking': row.rang,
            'pollution': row.poluare,
            'type': type_map[row.tip],
        })

    return rv
