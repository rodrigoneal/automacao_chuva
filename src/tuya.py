from enum import Enum
from typing import Any, Dict, List

from tuya_iot.openapi import TuyaOpenAPI
from tuya_iot import TuyaOpenAPI, AuthType


def comando(code: str, value: Any) -> Dict:
    """
    Faz o comando que é enviado no post da API
    Args:
        code (str): Codigo da API.
        value (Any): Valor da API.

    Returns:
        Dict: Dicionario com o comando pronto para enviar.
    """
    return {"commands": [{"code": code, "value": value}]}


class Color:
    """
    Classe com as cores da API.
    """

    RED = '{"h":0,"s":1000,"v":35}'
    WHITE = '{"h":0,"s":0,"v":1000}'
    YELLOW = '{"h":57,"s":1000,"v":99}'
    ORANGE = '{"h":27,"s":999,"v":100}'
    GREEN = '{"h": 88,"s": 1000,"v": 1000}'
    BLUE = '{"h": 220,"s": 1000,"v": 1000}'


class Code:
    """
    Classe com os codigos da API.
    """

    lampada = "switch_led"
    cor = "colour_data_v2"
    brilho = "bright_value_v2"
    contagem = "countdown_1"


class TuyaCommands:
    """
    Classe que interage com a API da tuya.
    """

    def __init__(
        self,
        ACCESS_ID: str,
        ACCESS_KEY: str,
        ENDPOINT: str,
        USERNAME: str,
        PASSWORD: str,
        DEVICE_ID: str,
    ) -> None:
        self.ACCESS_ID = ACCESS_ID
        self.ACCESS_KEY = ACCESS_KEY
        self.ENDPOINT = ENDPOINT
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.DEVICE_ID = DEVICE_ID
        self.openapi = self.config_api()
        self.code = Code()
        self.color = Color()
        self.comando = comando

    def config_api(self) -> TuyaOpenAPI:
        """
        Cria a conexão com a API da Tuya.

        Returns:
            TuyaOpenAPI:
        """
        openapi = TuyaOpenAPI(
            self.ENDPOINT, self.ACCESS_ID, self.ACCESS_KEY, AuthType.CUSTOM
        )
        openapi.connect(self.USERNAME, self.PASSWORD)
        return openapi

    def _encontrar_code(self, results: List[Dict], code: str) -> Dict:
        """
        Filtra o result retornado somente o code que deseja pegar.

        Args:
            results (List[Dict]): Lista com os dicionarios que deseja filtrar.
            code (str): Codigo do dicionario que deseja pegar.

        Returns:
            Dict: Dados filtrado.
        """
        for result in results:
            if result["code"] == code:
                return result
        return {"value": "Error"}

    def enviar_tuya(self, comando: Dict) -> bool:
        """
        Faz uma requisição POST enviando o comando para o servidor da tuya.
        Args:
            comando (str): comando que deseja enviar.

        Returns:
            bool: [description]
        """
        request = self.openapi.post(
            f"/v1.0/iot-03/devices/{self.DEVICE_ID}/commands", comando
        )
        return request["success"]

    def pegar_tuya(self, code: str) -> Dict:
        """
        Faz uma requisião GET no servidor da tuya e pega o status da lampada como cor, se está ligada e você pode passar
        o code para filtrar somente algo que deseja.

        Args:
            code (str): codigo que deseja filtrar.

        Returns:
            Dict: Com o status da lampada.
        """
        request = self.openapi.get(f"/v1.0/iot-03/devices/{self.DEVICE_ID}/status")
        return self._encontrar_code(request["result"], code)

    def ligar_lampada(self) -> bool:
        """Liga a lampada.

        Returns:
            bool: status da requisição.
        """
        comand = self.comando(self.code.lampada, True)
        return self.enviar_tuya(comand)

    def desligar_lampada(self) -> bool:
        """
        Desliga a lampada.
        Returns:
            bool: status da requisição.
        """
        comando = self.comando(self.code.lampada, False)
        return self.enviar_tuya(comando)

    def mudar_cor(self, cor: str) -> bool:
        """
        Muda a cor da lampada para a cor passada.
        OBS: primeiro você tem que ligar a lampada, essa função não liga.
        Args:
            cor (str): cor da lampada que deseja mudar.

        Returns:
            bool: status da requisição.
        """
        _cor = getattr(self.color, cor.upper())
        comando = self.comando(self.code.cor, _cor)
        return self.enviar_tuya(comando)

    @property
    def cor_lampada(self) -> str:
        """
        Property que retorna a da cor da lampada.
        Não mapeiei muitas cores(falta paciencia),
        Returns:
            str: cor da lampada em inglês.
        """
        cor = self.pegar_tuya("colour_data_v2")
        valor_cor = cor["value"]
        for k, v in Color.__dict__.items():
            if v == valor_cor:
                return k
        return "Error"

    @property
    def status_lampada(self) -> bool:
        """
        property que informa se a lampada está ligada ou desliga.
        Returns:
            bool: Se estiver ligada vai retornar True | False se estiver desligada.
        """
        status = self.pegar_tuya("switch_led")
        return status["value"]

    def timer_lampada(self, timer: int) -> bool:
        """
        Timer que liga ou desliga a lampada dependendo do status dela.
        Obs: O timer só aceita acima de 60 segundos, por isso faço o calculo para minutos.
        Args:
            timer (int): Tempo em segundos do timer.

        Returns:
            bool: Boleano informado se a requisição foi aceita.
        """

        comando = self.comando(self.code.contagem, timer)
        return self.enviar_tuya(comando)
