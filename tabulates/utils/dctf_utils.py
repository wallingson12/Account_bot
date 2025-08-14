import re

def limpar_valor(valor):
    if valor:
        valor = re.sub(r'[^\d.,]', '', valor)
        valor = valor.replace('.', '').replace(',', '.')
        return valor
    return ''
