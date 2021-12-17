from random import uniform

import pytest

from src.chuva import intensidade

@pytest.fixture
def forca():
    return intensidade
@pytest.mark.parametrize("valores", [uniform(50.1, 200) for _ in range(5)])
def test_se_intensidade_retorna_red(forca, valores):
    chuva = forca(valores)
    esperado = 'red'
    assert chuva == esperado

@pytest.mark.parametrize("valores", [uniform(25.1, 50.0) for _ in range(5)])
def test_se_intensidade_retorna_orange(forca, valores):
    chuva = forca(valores)
    esperado = 'orange'
    assert chuva == esperado

@pytest.mark.parametrize("valores", [uniform(5.0, 25.0) for _ in range(5)])
def test_se_intensidade_retorna_green(forca, valores):
    chuva = forca(valores)
    esperado = 'green'
    assert chuva == esperado

@pytest.mark.parametrize("valores", [uniform(0.1, 5.0) for _ in range(5)])
def test_se_intensidade_retorna_blue(forca, valores):
    chuva = forca(valores)
    esperado = 'blue'
    assert chuva == esperado

