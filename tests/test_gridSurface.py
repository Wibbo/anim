import pytest
from AppConfig import AppConfig
from GridSurface import GridSurface

@pytest.fixture
def resources():
    cfg = AppConfig
    gs = GridSurface(cfg)

    return gs


def test_get_inactive_cell_count_01(resources):
    cell_array = None
    resources.cell_array = None

    with pytest.raises(ValueError):
        resources.get_inactive_cell_count()


