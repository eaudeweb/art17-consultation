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


@pytest.mark.parametrize(
    'report_id',
    range(1, 8) + range(9, 16)
)
def test_reports(aggregation_app, report_id):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    url = '/raport/1/raport' + str(report_id)
    resp = client.get(url)
    assert resp.status_code == 200


@pytest.mark.xfail(raises=OperationalError)
def test_report_8(aggregation_app):
    _create_dataset(aggregation_app)
    client = aggregation_app.test_client()
    resp = client.get('/raport/1/raport8')
    assert resp.status_code == 200
