from typing import Callable


from typing import Callable
import time


import schedule


def agendar(tarefa: Callable) -> None:
    """
    Agenda uma tarefa que rodara a cada 10 minutos.
    Args:
        tarefa (Callable): Função que será chamada
    """
    schedule.every(15).minutes.do(tarefa)

    while True:
        schedule.run_pending()
        time.sleep(1)
