import pandas as pd

# --------------------------------------------
# Funções do validador.py (adaptadas para file_path)
# --------------------------------------------

def carregar_excel(file_path):
    return pd.read_excel(file_path)

def validar_colunas_valores(df):
    df['DelimitadordeRegistro'] = ''

    for idx, row in df.iterrows():
        try:
            base_calculo = float(str(row['Operações com Crédito do Imposto - Base de Cálculo']).replace(',', '.'))
            ipi_creditado = float(str(row['Operações com Crédito do Imposto - IPI Creditado']).replace(',', '.'))
            isentas = float(str(row['Operações sem Crédito do Imposto - Isentas ou Não Tributadas']).replace(',', '.'))
            outras = float(str(row['Operações sem Crédito do Imposto - Outras']).replace(',', '.'))

            if base_calculo > 0 and ipi_creditado == 0:
                df.at[idx, 'DelimitadordeRegistro'] = 'Foi necessário zerar a base'
                df.at[idx, 'Operações com Crédito do Imposto - Base de Cálculo'] = 0.0

            elif base_calculo == 0 and ipi_creditado == 0 and isentas == 0 and outras == 0:
                df.at[idx, 'DelimitadordeRegistro'] = 'Todas as colunas estão zeradas, certamente esse CFOP não será importado'

        except Exception as e:
            print(f"Erro na linha {idx}: {e}")

    return df

def formatar_dados(df):
    colunas_float = [
        'Operações com Crédito do Imposto - Base de Cálculo',
        'Operações com Crédito do Imposto - IPI Creditado',
        'Operações sem Crédito do Imposto - Isentas ou Não Tributadas',
        'Operações sem Crédito do Imposto - Outras'
    ]

    for col in colunas_float:
        df[col] = df[col].astype(float)

    colunas_14_digitos = [
        'CNPJ do Declarante',
        'CNPJ da Sucedida',
        'CNPJ do Estabelecimento Detentor do Crédito'
    ]
    for col in colunas_14_digitos:
        df[col] = df[col].astype(str).str.zfill(14)

    df['Período de Apuração'] = df['Período de Apuração'].astype(str).str.zfill(6)

    return df, colunas_float

# --------------------------------------------
# Funções do gerador de TXT
# --------------------------------------------

def format_field_11_12(value, start, end, field_type):
    length = end - start + 1
    if pd.isna(value):
        value = ''
    value = str(value).strip()

    if field_type == 'X':
        return value.ljust(length)[:length]
    elif field_type in ['CNPJ', 'XN', 'DATA', 'CFOP']:
        return value.zfill(length)[:length]
    elif field_type == 'R+':
        value = value.replace('.', '').replace(',', '')
        return value.zfill(length).ljust(length)[:length]
    elif field_type == 'EOL':
        return value.ljust(length)[:length]
    else:
        return value.ljust(length)[:length]

def generate_line(row):
    line = ''
    line += format_field_11_12(row['Tipo'], 1, 3, 'X')
    line += format_field_11_12(row['CNPJ do Declarante'], 4, 17, 'CNPJ')
    line += ' ' * 14
    line += format_field_11_12(row['CNPJ do Estabelecimento Detentor do Crédito'], 32, 45, 'CNPJ')

    periodo_apuracao = str(row['Período de Apuração']).strip().replace("'", "")
    if len(periodo_apuracao) == 5:
        periodo_apuracao = '0' + periodo_apuracao
    if len(periodo_apuracao) == 6:
        mes = periodo_apuracao[:2]
        ano = periodo_apuracao[2:]
    else:
        raise ValueError(f"Formato de 'Período de Apuração' inválido: {periodo_apuracao}")

    line += format_field_11_12(ano, 46, 49, 'XN')
    line += format_field_11_12(mes, 50, 51, 'XN')
    line += format_field_11_12(row['Decêndio/Quinzena do Período de Apuração'], 52, 52, 'X')
    line += format_field_11_12(row['CFOP'], 53, 56, 'CFOP')
    line += format_field_11_12(row['Operações com Crédito do Imposto - Base de Cálculo'], 57, 70, 'R+')
    line += format_field_11_12(row['Operações com Crédito do Imposto - IPI Creditado'], 71, 84, 'R+')
    line += format_field_11_12(row['Operações sem Crédito do Imposto - Isentas ou Não Tributadas'], 85, 98, 'R+')
    line += format_field_11_12(row['Operações sem Crédito do Imposto - Outras'], 99, 112, 'R+')
    line += '\n'
    return line