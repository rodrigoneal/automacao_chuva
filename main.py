from dotenv import dotenv_values


from src.alerta import pegar_clima
from src.chuva import intensidade
from src.info import info_prox
from src.message import enviar_mensagem
from src.run import agendar
from src.tuya import TuyaCommands

config = dotenv_values(".env")

ACCESS_ID = config["ACCESS_ID"]
ACCESS_KEY = config["ACCESS_KEY"]
ENDPOINT = config["ENDPOINT"]
USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]
DEVICE_ID = config["DEVICE_ID"]
token = config["API_TOKEN"]


tuya = TuyaCommands(ACCESS_ID, ACCESS_KEY,
                    ENDPOINT, USERNAME, PASSWORD,
                    DEVICE_ID)  # type:ignore


def run():
    """
    Função que faz o programa funcionar.
    """
    elementos = pegar_clima()
    maior = max([elemento.chuva for elemento in elementos])
    intensidade_chuva = intensidade(maior)  # type:ignore
    if intensidade_chuva != "black":
        tuya.ligar_lampada()
        tuya.mudar_cor(intensidade_chuva)
        [enviar_mensagem(elemento,token) for elemento in elementos]
        tuya.timer_lampada(10)
    else:
        tuya.desligar_lampada()
    print(info_prox())
    print(elementos)


if __name__ == "__main__":
    try:
        agendar(run)
    except:
        tuya.desligar_lampada()
