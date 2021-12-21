from datetime import datetime
import random

import pytest

from src.elemento import Elemento

bairros = [
    "Irajá",
    "Madureira",
    "Bangu",
    "Campo Grande",
    "Av. Brasil/Mendanha",
    "Santa Cruz",
]


@pytest.fixture
def gera_bairro():
    return random.choice(bairros)


@pytest.fixture
def gera_chuva():
    return f"{random.uniform(0, 200):.2f}"


@pytest.fixture
def gera_hora():
    hora = str(random.randint(0, 23))
    minuto = str(random.randint(0, 59))
    return hora + ":" + minuto


@pytest.fixture
def retorna_elemento(gera_bairro, gera_chuva, gera_hora):
    return Elemento(gera_bairro, gera_hora, gera_chuva)


def test_se_elemento_muda_chuva_str_para_float(retorna_elemento):
    elemento = retorna_elemento
    assert isinstance(elemento.chuva, float)


def test_se_elemento_muda_hora_para_str(retorna_elemento):
    elemento = retorna_elemento
    assert isinstance(elemento.hora, str)


def test_se_elemento_retorna_0_ponto_0_se_passar_um_valor_de_chuva_invalido(
    retorna_elemento,
):
    elemento = Elemento("Irajá", "08:10", "None")
    esperado = 0.0
    assert elemento.chuva == esperado
