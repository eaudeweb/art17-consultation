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
    resp = client.get('/raport/1/raport1')
    assert resp.status_code == 200


def test_report_2(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport2')
    assert resp.status_code == 200


def test_report_3(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport3')
    assert resp.status_code == 200


def test_report_4(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport4')
    assert resp.status_code == 200


def test_report_5(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport5')
    assert resp.status_code == 200


def test_report_6(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport6')
    assert resp.status_code == 200


def test_report_7(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport7')
    assert resp.status_code == 200


@pytest.mark.xfail(raises=OperationalError)
def test_report_8(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport8')
    assert resp.status_code == 200


def test_report_9(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport9')
    assert resp.status_code == 200


def test_report_10(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport10')
    assert resp.status_code == 200


def test_report_11(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport11')
    assert resp.status_code == 200


def test_report_12(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport12')
    assert resp.status_code == 200


def test_report_13(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport13')
    assert resp.status_code == 200


def test_report_14(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport14')
    assert resp.status_code == 200


def test_report_15(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport15')
    assert resp.status_code == 200
