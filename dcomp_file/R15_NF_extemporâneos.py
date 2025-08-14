import pandas as pd

# Função para formatar os campos conforme especificações
def format_field_15(value, start, end, field_type):
    length = end - start + 1
    if pd.isna(value):
        value = ''  # Trata valores ausentes
    value = str(value).strip()

    if field_type == 'X':
        return value.ljust(length)[:length]
    elif field_type in ['CNPJ', 'XN', 'DATA', 'CFOP']:
        return value.zfill(length)[:length]
    elif field_type == 'R+':
        value = value.replace('.', '').replace(',', '')
        return value.zfill(length).ljust(length)[:length]
    elif field_type == 'CRED':
        return value.ljust(length)[:length]  # Para campo "CRED", só usa preenchimento de espaços
    elif field_type == 'DECENDIO1':
        return value.zfill(length)[:length]
    elif field_type == 'MM':
        return value.zfill(length)[:length]
    elif field_type == 'AAAA':
        return value.zfill(length)[:length]
    elif field_type == 'EOL':
        return value.ljust(length)[:length]
    else:
        return value.ljust(length)[:length]

# Função para formatar datas
def format_date(value):
    if pd.isna(value):
        return ''
    if isinstance(value, pd.Timestamp):
        return value.strftime('%d%m%Y')
    return value.replace('/', '')

# Função para gerar uma linha formatada
def generate_line(row):
    line = ''
    line += format_field_15(row['Tipo'], 1, 3, 'X')  # Tipo
    line += format_field_15(row['CNPJ do Declarante'], 4, 17, 'CNPJ')  # CNPJ do Declarante
    line += ' ' * 14  # 14 espaços vazios
    # line += format_field_15(row['CNPJ da Sucedida'], 18, 31, 'CNPJ')  # CNPJ da Sucedida
    line += format_field_15(row['CNPJ do Estabelecimento Detentor do Crédito'], 32, 45, 'CNPJ')  # CNPJ do Estabelecimento Detentor
    line += format_field_15(row['CNPJ do Emitente'], 46, 59, 'CNPJ')  # CNPJ do Emitente
    line += format_field_15(row['Nº da Nota Fiscal'], 60, 68, 'XN')  # Nº da Nota Fiscal
    line += format_field_15(row['Série/Subsérie'], 69, 71, 'X')  # Série/Subsérie
    line += format_field_15(row['Data de Emissão'], 72, 79, 'DATA')  # Data de Emissão
    line += format_field_15(row['Data de Entrada no Estabelecimento Detentor do Crédito'], 80, 87, 'DATA')  # Data de Entrada
    line += format_field_15(row['CFOP'], 88, 91, 'CFOP')  # CFOP
    line += format_field_15(row['Valor Total'], 92, 105, 'R+')  # Valor Total
    line += format_field_15(row['Valor do IPI Destacado'], 106, 119, 'R+')  # Valor do IPI Destacado
    line += format_field_15(row['Valor do IPI Creditado no Livro RAIPI'], 120, 133, 'R+')  # Valor do IPI Creditado
    line += format_field_15(row['Espécie do Crédito'], 134, 134, 'CRED')  # Espécie do Crédito
    line += format_field_15(row['Decêndio/Quinzena do Período de Escrituração'], 135, 135, 'DECENDIO1')  # Decêndio/Quinzena
    line += format_field_15(row['Mês do Período de Escrituração'], 136, 137, 'MM')  # Mês
    line += format_field_15(row['Ano do Período de Escrituração'], 138, 141, 'AAAA')  # Ano
    line += '\n'  # Adiciona uma nova linha

    return line

# Função para processar o arquivo Excel e gerar o arquivo TXT
def process_file_15(file_path):
    df = pd.read_excel(file_path)

    # Formatação das colunas de data
    df['Data de Emissão'] = df['Data de Emissão'].apply(format_date)
    df['Data de Entrada no Estabelecimento Detentor do Crédito'] = df['Data de Entrada no Estabelecimento Detentor do Crédito'].apply(format_date)

    # Formatação das colunas de valor
    df['Valor Total'] = df['Valor Total'].apply(lambda x: f'{x:,.2f}'.replace('.', ','))
    df['Valor do IPI Destacado'] = df['Valor do IPI Destacado'].apply(lambda x: f'{x:,.2f}'.replace('.', ','))
    df['Valor do IPI Creditado no Livro RAIPI'] = df['Valor do IPI Creditado no Livro RAIPI'].apply(lambda x: f'{x:,.2f}'.replace('.', ','))

    # Geração do conteúdo do arquivo TXT
    lines = df.apply(generate_line, axis=1)

    # Obtém o valor da coluna 'Tipo' da primeira linha
    file_type = df['Tipo'].iloc[0]

    # Define o caminho do arquivo de saída com base no valor da coluna 'Tipo'
    output_path = rf"{file_type}.txt"
    with open(output_path, "w") as file:
        file.writelines(lines)

    return output_path