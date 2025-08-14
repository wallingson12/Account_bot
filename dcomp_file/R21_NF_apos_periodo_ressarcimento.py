import pandas as pd

# Função para formatar os campos conforme especificações
def format_field_21(value, start, end, field_type):
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
    elif field_type == 'DECENDIO2':
        return value.zfill(length)[:length]
    elif field_type == 'MM':
        return value.zfill(length)[:length]
    elif field_type == 'AAAA':
        return value.zfill(length)[:length]
    elif field_type == 'EOL':
        return value.ljust(length)[:length]
    elif field_type == 'N':
        return value.ljust(length)[:length]  # Para campo N, só usa preenchimento de espaços
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
    line += format_field_21(row['Tipo'], 1, 3, 'X')  # Tipo
    line += format_field_21(row['CNPJ do Declarante'], 4, 17, 'CNPJ')  # CNPJ do Declarante
    line += ' ' * 14  # 14 espaços vazios
    line += format_field_21(row['CNPJ do Estabelecimento Detentor do Crédito'], 32, 45, 'CNPJ')  # CNPJ do Declarante
    line += format_field_21(row['Ano do Período de Apuração'], 46, 49, 'AAAA')  # Ano do Período de Apuração
    line += format_field_21(row['Mês do Período de Apuração'], 50, 51, 'MM')  # Mês do Período de Apuração
    line += format_field_21(row['Decêndio/Quinzena do Período de Apuração'], 52, 52, 'DECENDIO2')  # Decêndio/Quinzena
    line += format_field_21(row['Existe Movimento no Período?'], 53, 53, 'N')  # Existe Movimento no Período?
    line += format_field_21(row['Demonstrativo de Créditos - Por Entradas do Mercado Nacional'], 54, 67, 'R+')  # Entradas Mercado Nacional
    line += format_field_21(row['Demonstrativo de Créditos - Por Entradas do Mercado Externo'], 68, 81, 'R+')  # Entradas Mercado Externo
    line += format_field_21(row['Demonstrativo de Créditos - Estorno de Débitos'], 82, 95, 'R+')  # Estorno de Débitos
    line += format_field_21(row['Demonstrativo de Créditos - Crédito Presumido'], 96, 109, 'R+')  # Crédito Presumido
    line += format_field_21(row['Demonstrativo de Créditos - Créditos Extemporâneos'], 110, 123, 'R+')  # Créditos Extemporâneos
    line += format_field_21(row['Demonstrativo de Créditos - Demais Créditos'], 124, 137, 'R+')  # Demais Créditos
    line += format_field_21(row['Demonstrativo de Débitos - Por Saídas para o Mercado Nacional'], 138, 151, 'R+')  # Saídas Mercado Nacional
    line += format_field_21(row['Demonstrativo de Débitos - Estorno de Créditos'], 152, 165, 'R+')  # Estorno de Créditos
    line += format_field_21(row['Demonstrativo de Débitos - Ressarcimentos de Créditos'], 166, 179, 'R+')  # Ressarcimentos de Créditos
    line += format_field_21(row['Demonstrativo de Débitos - Outros Débitos'], 180, 193, 'R+')  # Outros Débitos
    line += '\n'  # Adiciona uma nova linha

    return line

# Função para processar o arquivo Excel e gerar o arquivo TXT
def process_file_21(file_path):
    df = pd.read_excel(file_path)

    # Geração do conteúdo do arquivo TXT
    lines = df.apply(generate_line, axis=1)

    # Obtém o valor da coluna 'Tipo' da primeira linha
    file_type = df['Tipo'].iloc[0]

    # Define o caminho do arquivo de saída com base no valor da coluna 'Tipo'
    output_path = rf"{file_type}.txt"
    with open(output_path, "w") as file:
        file.writelines(lines)

    return output_path