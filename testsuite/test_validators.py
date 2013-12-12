from werkzeug.datastructures import MultiDict
import pytest


NOT_VALID = object()


@pytest.mark.parametrize(['formdata', 'valid_data'], [
    # all values are blank
    [{'trend': '', 'period.start': '', 'period.end': ''},
     {'trend': '', 'period': {'start': None, 'end': None},
     'magnitude': {'min': None, 'max': None}}],

    # trend and both years filled in
    [{'trend': '+', 'period.start': '2010', 'period.end': '2013'},
     {'trend': '+', 'period': {'start': 2010, 'end': 2013},
     'magnitude': {'min': None, 'max': None}}],

    # years filled in with bogus data
    [{'trend': '+', 'period.start': 'asdf', 'period.end': 'qwer'},
     NOT_VALID],

    # years filled in with bogus numeric
    [{'trend': '+', 'period.start': '13', 'period.end': '123456'},
     NOT_VALID],

    # only first year filled in
    [{'trend': '+', 'period.start': '2010', 'period.end': ''},
     NOT_VALID],

    # only second year filled in
    [{'trend': '+', 'period.start': '', 'period.end': '2013'},
     NOT_VALID],

    # years filled in but no trend
    [{'trend': '', 'period.start': '2010', 'period.end': '2013'},
     NOT_VALID],

    # trend filled in but no years
    [{'trend': '+', 'period.start': '', 'period.end': ''},
     NOT_VALID],
])
def test_trend_validation(formdata, valid_data):
    from art17 import forms
    form = forms.Trend(MultiDict(formdata))

    if valid_data is NOT_VALID:
        assert not form.validate()

    else:
        assert form.validate()
        assert form.data == valid_data


@pytest.mark.parametrize(['formdata', 'valid_data'], [
    # all values are blank
    [{'op': '', 'number': '', 'method': ''},
     {'op': '', 'number': None, 'method': ''}],

    # both values filled in
    [{'op': 'foo', 'number': '1234', 'method': ''},
     {'op': 'foo', 'number': 1234, 'method': ''}],

    # only op filled in
    [{'op': 'foo', 'number': '', 'method': ''},
     NOT_VALID],

    # only number filled in
    [{'op': '', 'number': '1234', 'method': ''},
     NOT_VALID],
])
def test_reference_value_validation(formdata, valid_data):
    from art17 import forms
    form = forms.ReferenceValue(MultiDict(formdata))
    form.op.choices = [('', ''), ('foo', 'Foo'), ('bar', 'Bar')]

    if valid_data is NOT_VALID:
        assert not form.validate()

    else:
        assert form.validate()
        assert form.data == valid_data
