from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Elemento:
    local: str
    hora: str
    chuva: str

    def change_value(self, value: str) -> float:
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return 0.0

    def parser_hour(self, value: str) -> str:
        hora = int(value.split(":")[0])
        minuto = int(value.split(":")[1])
        tempo = datetime.now().replace(
            hour=hora, minute=minuto, second=0, microsecond=0
        )
        return tempo.strftime("%d/%m/%Y %H:%M")

    def __post_init__(self):
        self.chuva = self.change_value(self.chuva)
        self.hora = self.parser_hour(self.hora)
