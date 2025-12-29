import pandas as pd

def format_field(value, start, end, field_type):
    # Calcula o tamanho do campo com base nas posições inicial e final
    length = end - start + 1
    # Se o valor for NaN (vazio), substitui por string vazia
    if pd.isna(value):
        value = ''
    # Se o valor for NaN (vazio), substitui por string vazia
    value = str(value).strip()


    # Para campos de texto ou especiais
    # Preenche com espaços à direita até atingir o tamanho definido
    if field_type in ['X', 'CRED', 'N']:
        return value.ljust(length)[:length]

    # Para campos numéricos, códigos ou datas
    # Preenche com zeros à esquerda até o tamanho definido
    elif field_type in ['CNPJ', 'XN', 'DATA', 'CFOP', 'MM', 'AAAA', 'DECENDIO1', 'DECENDIO2']:
        return value.zfill(length)[:length]
    # Para valores monetários ('R+')
    # Remove pontos e vírgulas e preenche com zeros à esquerda
    elif field_type == 'R+':
        value = value.replace('.', '').replace(',', '')
        return value.zfill(length)[:length]
    elif field_type == 'SPACE':
        return ' ' * length
    # Caso padrão: trata como texto e preenche com espaços à direita
    return value.ljust(length)[:length]


def format_date(value):
    # Se o valor for NaN (vazio), retorna string vazia
    if pd.isna(value):
        return ''

    # Se o valor for um timestamp do pandas (data/hora), formata como 'ddmmaaaa'
    if isinstance(value, pd.Timestamp):
        return value.strftime('%d%m%Y')

    # Caso seja uma string ou outro tipo, remove as barras '/' da data
    return str(value).replace('/', '')