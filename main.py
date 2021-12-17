from dotenv import dotenv_values


from src.alerta import pegar_clima
from src.chuva import intensidade
from src.run import agendar
from src.tuya import TuyaCommands


config = dotenv_values(".env")
tuya = TuyaCommands(**config)  # type:ignore


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
    else:
        tuya.desligar_lampada()
    print(elementos)


if __name__ == "__main__":
    agendar(run)
