import pytest
import math

from image_processing import Processing


@pytest.fixture
def processing():
    return Processing("spot.png")


@pytest.fixture
def std(processing):
    return processing.std


@pytest.fixture
def dispersion(processing):
    return processing.disp


@pytest.fixture
def real_coord_x(processing):
    return processing.real_x


@pytest.fixture
def real_coord_y(processing):
    return processing.real_y


@pytest.fixture
def defined_coord_x(processing):
    return processing.x


@pytest.fixture
def defined_coord_y(processing):
    return processing.y


def test_dispersion(std, dispersion):
    std_value = std
    dispersion_value = dispersion

    assert dispersion_value == std_value ** 2, (" Дисперсия должна быть равна квадрату среднеквадратичного отклонения "
                                                " Проверь yaml файл")


def test_std(std, dispersion):
    std_value = std
    dispersion_value = dispersion

    assert std_value == math.sqrt(dispersion_value), (
        " Среднеквадратичное отклонение является квадратным корнем из дисперсии "
        " Проверь yaml файл ")


def test_coordinates_x(real_coord_x, defined_coord_x):
    real_x = real_coord_x
    defined_x = defined_coord_x

    assert real_x == defined_x, " Реальные координаты центра пятна по оси x отличаются от заданных в yaml "


def test_coordinates_y(real_coord_y, defined_coord_y):
    real_y = real_coord_y
    defined_y = defined_coord_y

    assert real_y == defined_y, " Реальные координаты центра пятна по оси y отличаются от заданных в yaml "
