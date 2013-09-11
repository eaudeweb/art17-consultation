from conftest import Obj
from mock import Mock


def test_parse_blank_period():
    from art17.schemas import parse_period
    obj = Mock(foo_period=None)
    assert parse_period(obj, 'foo_period') is None


def test_flatten_blank_period():
    from art17.schemas import flatten_period
    obj = Obj()
    flatten_period(None, obj, 'foo_period')
    assert obj.foo_period is None
    flatten_period({'start': None, 'end': None}, obj, 'foo_period')
    flatten_period({'start': '', 'end': ''}, obj, 'foo_period')
    assert obj.foo_period is None
