import pytest
import time
import math

from image_processing import Processing


def test_dispersion():

    processing = Processing()

    std_value = processing.std
    dispersion_value = processing.disp


    assert dispersion_value == std_value ** 2

