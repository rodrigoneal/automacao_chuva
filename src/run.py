import time
from typing import Callable


import schedule

from src.info import info_prox


def agendar(tarefa: Callable) -> None:
    """
    Agenda uma tarefa que rodara a cada 10 minutos.
    Args:
        tarefa (Callable): Função que será chamada
    """
    print(info_prox())
    schedule.every(15).minutes.do(tarefa)

    while True:
        schedule.run_pending()
        time.sleep(1)
