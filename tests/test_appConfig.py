import pytest
from AppConfig import AppConfig


@pytest.fixture
def app_settings():
    cfg = AppConfig('../GoL.ini')
    return cfg


def test_string_to_boolean_01():
    with pytest.raises(KeyError):
        AppConfig.string_to_boolean('Not true')


def test_string_to_boolean_02():
    with pytest.raises(KeyError):
        AppConfig.string_to_boolean('1')


def test_string_to_boolean_03():
    with pytest.raises(KeyError):
        AppConfig.string_to_boolean('0')


def test_string_to_boolean_04():
    assert AppConfig.string_to_boolean('True') == True


def test_string_to_boolean_05():
    assert AppConfig.string_to_boolean('False') == False














