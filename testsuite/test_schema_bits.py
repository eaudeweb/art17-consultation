from conftest import Obj

def test_parse_blank_period():
    from art17 import schemas
    split_period = schemas.GenericRecord._split_period
    assert split_period(None) is None


def test_flatten_blank_period():
    from art17.schemas import flatten_period
    obj = Obj()
    flatten_period(None, obj, 'foo_period')
    assert obj.foo_period is None
    flatten_period({'start': None, 'end': None}, obj, 'foo_period')
    flatten_period({'start': '', 'end': ''}, obj, 'foo_period')
    assert obj.foo_period is None
