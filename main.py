from dotenv import dotenv_values


from src.alerta import pegar_clima
from src.chuva import intensidade
from src.tuya import TuyaCommands


config = dotenv_values(".env")

tuya = TuyaCommands(**config)  # type:ignore

elementos = pegar_clima()
maior = max([elemento.chuva for elemento in elementos])
intensidade_chuva = intensidade(maior)  # type:ignore
if intensidade_chuva != "black":
    tuya.ligar_lampada()
    tuya.mudar_cor(intensidade_chuva)
