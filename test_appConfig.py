import pytest
from configuration import AppConfig


@pytest.fixture
def app_settings():
    cfg = AppConfig('GoL.ini')
    return cfg


def test_minimum_row_count(app_settings):
    assert app_settings.row_count >= 2


def test_maximum_row_count(app_settings):
    assert app_settings.row_count <= 200


def test_minimum_column_count(app_settings):
    assert app_settings.column_count >= 2


def test_maximum_column_count(app_settings):
    assert app_settings.column_count <= 400


def test_minimum_window_width(app_settings):
    assert app_settings.initial_screen_width >= 200


def test_maximum_window_width(app_settings):
    assert app_settings.initial_screen_width <= 2400


def test_minimum_window_height(app_settings):
    assert app_settings.initial_screen_height >= 200


def test_maximum_window_height(app_settings):
    assert app_settings.initial_screen_height <= 1024


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


def test_line_width(app_settings):
    assert app_settings.line_width == 1










