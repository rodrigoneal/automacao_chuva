from datetime import datetime, timedelta

def info_prox()->str:
    proximo = datetime.now() + timedelta(minutes=15)
    prox_str = proximo.strftime("%d/%m/%Y %H:%M:%S")
    return prox_str