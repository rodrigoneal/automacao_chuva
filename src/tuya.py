from typing import Any, Dict, List

from tuya_iot import TuyaOpenAPI, AuthType


def comando(code: str, value: Any) -> Dict:
    return {'commands': [{'code': code, "value": value}]}

class Color:
    red = "{\"h\":0,\"s\":1000,\"v\":35}"
    white = "{\"h\":0,\"s\":0,\"v\":1000}"
    yellow = "{\"h\":57,\"s\":100,\"v\":99}"
    orange = "{\"h\":30,\"s\":99,\"v\":100}"

class Code:
    lampada = 'switch_led'
    cor = 'colour_data_v2'
    brilho = 'bright_value_v2'
    contagem = 'countdown_1'



class TuyaCommands:
    
    def __init__(self, ACCESS_ID: str, ACCESS_KEY: str,
                 ENDPOINT: str, USERNAME: str,
                 PASSWORD: str, DEVICE_ID: str) -> None:
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

    def config_api(self):
        openapi = TuyaOpenAPI(self.ENDPOINT, self.ACCESS_ID,
                              self.ACCESS_KEY, AuthType.CUSTOM)
        openapi.connect(self.USERNAME, self.PASSWORD)
        return openapi

    def _encontrar_code(self, results: List[Dict], code: str) -> Dict:
        for result in results:
            if result['code'] == code:
                return result

    def enviar_tuya(self, comando: str) -> bool:
        request = self.openapi.post(
            f'/v1.0/iot-03/devices/{self.DEVICE_ID}/commands', comando)
        return request['success']

    def pegar_tuya(self, code: str) -> Dict:
        request = self.openapi.get(
            f'/v1.0/iot-03/devices/{self.DEVICE_ID}/status')
        return self._encontrar_code(request['result'], code)

    def ligar_lampada(self):
        comand = self.comando(self.code.lampada, True)
        return self.enviar_tuya(comand)

    def desligar_lampada(self):
        comando = self.comando(self.code.lampada, False)
        return self.enviar_tuya(comando)

    def mudar_cor_vermelho(self):
        comando = self.comando(self.code.cor, self.color.red)
        return self.enviar_tuya(comando)

    def mudar_cor_branco(self):
        comando = self.comando(self.code.cor, self.color.white)
        return self.enviar_tuya(comando)

    @property
    def cor_lampada(self) -> str:
        cor = self.pegar_tuya('colour_data_v2')
        valor_cor = cor['value']
        for k, v in Color.__dict__.items():
            if v == valor_cor:
                return k.title()

    @property
    def status_lampada(self) -> bool:
        status = self.pegar_tuya('switch_led')
        return status['value']
    
    def timer_lampada(self, timer: int):
        comando = self.comando(self.code.contagem, timer)
        return self.enviar_tuya(comando)

    
