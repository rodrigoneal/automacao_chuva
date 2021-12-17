from dotenv import dotenv_values
import pytest
from time import sleep

from src.tuya import TuyaCommands

@pytest.fixture
def tuya_comando():
    config = dotenv_values(".env")
    tuya = TuyaCommands(**config)
    yield tuya
    tuya.mudar_cor_branco()
    tuya.desligar_lampada()

def test_se_liga_a_lampada(tuya_comando):
    tuya = tuya_comando
    assert tuya.ligar_lampada()

def test_se_desliga_a_lampada(tuya_comando):
    tuya = tuya_comando
    assert tuya.desligar_lampada()

def test_se_retorna_o_status_da_lampada(tuya_comando):
    tuya = tuya_comando
    result = tuya.pegar_tuya('switch_led')
    esperado = {'code': 'switch_led', 'value': False}
    assert result == esperado

def test_se_status_lampada_retorna_false(tuya_comando):
    tuya = tuya_comando
    lampada = tuya.status_lampada
    esperado = False
    assert lampada == esperado

def test_se_lampada_muda_cor_para_vermelho(tuya_comando):
    tuya = tuya_comando
    tuya.ligar_lampada()
    result = tuya.mudar_cor_vermelho()
    esperado = True
    assert result == esperado

def test_se_retorna_cor_lampada(tuya_comando):
    tuya = tuya_comando
    cor = tuya.cor_lampada
    esperado = 'White'
    assert cor == esperado

def test_se_lampada_desliga_em_5_segundos(tuya_comando):
    tuya = tuya_comando
    status_1 = tuya.status_lampada
    tuya.timer_lampada(60)
    sleep(61)
    status_2 = tuya.status_lampada
    assert status_1 != status_2
