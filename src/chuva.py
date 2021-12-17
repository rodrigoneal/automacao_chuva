def intensidade(chuva):
    muito_forte = 50.0
    forte = 25.1
    moderada = 5.0
    fraca = 0.1
    if chuva >= muito_forte:
        return 'red'
    elif chuva < muito_forte and chuva >= forte:
        return 'orange'
    elif chuva < forte and chuva >= moderada:
        return 'green'
    elif chuva < moderada and chuva >= fraca:
        return 'blue'