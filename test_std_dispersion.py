import pytest
import time
import math

from image_processing import Processing


@pytest.fixture
def processing():
    return Processing()


@pytest.fixture
def std(processing):
    return processing.std


@pytest.fixture
def dispersion(processing):
    return processing.disp


def test_dispersion(std, dispersion):

    std_value = std
    dispersion_value = dispersion

    assert dispersion_value == std_value ** 2, " Дисперсия олжна быть равна квадрату среднеквадратичного отклонения "


def test_std(std, dispersion):

    std_value = std
    dispersion_value = dispersion

    assert std_value == math.sqrt(dispersion_value), ""
