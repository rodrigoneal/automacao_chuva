from dotenv import dotenv_values


from src.alerta import pegar_clima
from src.chuva import intensidade
from src.tuya import TuyaCommands


config = dotenv_values(".env")

tuya = TuyaCommands(**config)

elementos = pegar_clima()


