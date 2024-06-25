import pytest
import time
import math

from image_processing import Processing


def test_variance():

    processing = Processing()

    std_value = processing.std
    dispersion_value = processing.dispersion


    assert not math.isclose(std_value ** 2, dispersion_value)

