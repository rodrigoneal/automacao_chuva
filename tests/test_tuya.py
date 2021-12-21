from dotenv import dotenv_values
import pytest
from time import sleep
from random import choice

from src.tuya import TuyaCommands


@pytest.fixture
def tuya_comando():

    config = dotenv_values(".env")
    ACCESS_ID = config["ACCESS_ID"]
    ACCESS_KEY = config["ACCESS_KEY"]
    ENDPOINT = config["ENDPOINT"]
    USERNAME = config["USERNAME"]
    PASSWORD = config["PASSWORD"]
    DEVICE_ID = config["DEVICE_ID"]
    tuya = TuyaCommands(ACCESS_ID, ACCESS_KEY, ENDPOINT, USERNAME, PASSWORD, DEVICE_ID)
    yield tuya
    tuya.mudar_cor("WHITE")
    tuya.desligar_lampada()


cores = ["WHITE", "YELLOW", "ORANGE", "RED"]


def test_se_liga_a_lampada(tuya_comando):
    tuya = tuya_comando
    assert tuya.ligar_lampada()


def test_se_desliga_a_lampada(tuya_comando):
    tuya = tuya_comando
    assert tuya.desligar_lampada()


def test_se_retorna_o_status_da_lampada(tuya_comando):
    tuya = tuya_comando
    result = tuya.pegar_tuya("switch_led")
    esperado = {"code": "switch_led", "value": False}
    assert result == esperado


def test_se_status_lampada_retorna_false(tuya_comando):
    tuya = tuya_comando
    lampada = tuya.status_lampada
    esperado = False
    assert lampada == esperado


@pytest.mark.parametrize("cor", [choice(cores) for _ in range(5)])
def test_se_lampada_muda_cor(tuya_comando, cor):
    tuya = tuya_comando
    tuya.ligar_lampada()
    tuya.mudar_cor(cor)
    sleep(1)
    esperado = tuya.cor_lampada
    assert cor == esperado


def test_se_retorna_cor_lampada(tuya_comando):
    tuya = tuya_comando
    cor = tuya.cor_lampada
    esperado = "WHITE"
    assert cor == esperado


def test_se_lampada_desliga_em_60_segundos(tuya_comando):
    tuya = tuya_comando
    status_1 = tuya.status_lampada
    tuya.timer_lampada(60)
    sleep(61)
    status_2 = tuya.status_lampada
    assert status_1 != status_2
