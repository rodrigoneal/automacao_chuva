from pushbullet import Pushbullet
from src.elemento import Elemento


def enviar_mensagem(elemento: Elemento, token:str) -> None:
    """Função que envia um alerta da chuva pelo pushbullet.

    Args:
        elemento (Elemento): Elemento com os dados da chuva.
    """
    pb = Pushbullet(token)
    mensangem = f"Em {elemento.local} na ultima hora choveu {elemento.chuva}mm"
    pb.push_note("Alerta Chuva", mensangem, pb.devices[0])

