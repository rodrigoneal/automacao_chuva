from dataclasses import dataclass
from typing import Any

@dataclass
class Elemento:
    local: str
    chuva: str

    def change_value(self, value: str)-> float:
        try:
            return float(value.replace(',', '.'))
        except ValueError:
            return 0.0

    def __post_init__(self):
        self.chuva = self.change_value(self.chuva)
