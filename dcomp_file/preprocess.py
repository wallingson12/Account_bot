from .formatter import format_date

def format_record(df, style='r13'):
    """
    Formata datas e valores monetários do DataFrame.
    style: 'r13' ou 'r15'
    """
    date_cols = ['Data de Emissão', 'Data de Entrada no Estabelecimento Detentor do Crédito']
    value_cols = ['Valor Total', 'Valor do IPI Destacado', 'Valor do IPI Creditado no Livro RAIPI']

    # Formata datas
    for col in date_cols:
        df[col] = df[col].apply(format_date)

    # Formata valores
    if style == 'r13':
        for col in value_cols:
            df[col] = df[col].apply(lambda x: f'{x:,.2f}'.replace('.', ','))
    elif style == 'r15':
        for col in value_cols:
            df[col] = df[col].apply(lambda x: f'{float(x):,.2f}'.replace('.', '').replace(',', ''))
        # adiciona zfill de mês/ano
        df['Mês do Período de Escrituração'] = df['Mês do Período de Escrituração'].astype(str).str.zfill(2)
        df['Ano do Período de Escrituração'] = df['Ano do Período de Escrituração'].astype(str).str.zfill(4)

    return df