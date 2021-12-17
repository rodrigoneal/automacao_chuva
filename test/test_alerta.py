import pytest

from src.alerta import pegar_clima, Elemento


@pytest.fixture(scope="module")
def clima():
    pegar = pegar_clima()
    return pegar


def test_se_retorna_pegar_clima_retorna_uma_lista(clima):
    pegar = clima
    esperado = list
    assert isinstance(pegar, esperado)


def test_se_retorna_uma_lista_de_elementos(clima):
    pegar = clima
    esperado = Elemento
    assert all(isinstance(p, esperado) for p in pegar)
