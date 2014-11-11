import pytest
from sqlalchemy.exc import OperationalError

from art17 import models


def _create_dataset(aggregation_app):
    with aggregation_app.app_context():
        dataset = models.Dataset(id=1, status='')
        models.db.session.add(dataset)
        models.db.session.commit()


def test_report_home(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1')
    assert resp.status_code == 200


def test_report_1(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/missing')
    assert resp.status_code == 200


def test_report_8(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/validation')
    assert resp.status_code == 200


def test_report_10(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/bioreg_annex')
    assert resp.status_code == 200


def test_report_11(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/conservation_status')
    assert resp.status_code == 200


def test_report_12(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/bioreg_global')
    assert resp.status_code == 200


def test_report_13(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/13')
    assert resp.status_code == 200


def test_report_14(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/14')
    assert resp.status_code == 200


@pytest.mark.xfail(raises=OperationalError)
def test_report_15(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/15')
    assert resp.status_code == 200


def test_report_16(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/16')
    assert resp.status_code == 200


def test_report_17(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/17')
    assert resp.status_code == 200


def test_report_18(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/pressures1')
    assert resp.status_code == 200


def test_report_20(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/measures')
    assert resp.status_code == 200


def test_report_21(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/measures_effects')
    assert resp.status_code == 200


def test_report_22(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/quality')
    assert resp.status_code == 200


def test_report_23(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/statistics23')
    assert resp.status_code == 200
