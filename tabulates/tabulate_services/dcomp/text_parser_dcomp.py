import re

def extrair_dados_texto_dcomp(texto):
    regex_patterns = {
        'CNPJ': r'CNPJ\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})',
        'D ou C': r'001\. (Débito|Crédito)\s*(.*)',
        'Data de Transmissão': r'Data de Transmissão\s*(\d{2}/\d{2}/\d{4})',
        'Nome Empresarial': r'Nome Empresarial\s*(.*)',
        'Informado em Outro PER/DCOMP': r'Informado em Outro PER/DCOMP\s*(.*)',
        'PER/DCOMP Retificador': r'PER/DCOMP Retificador\s*(Sim|Não)',
        'Período de Apuração': r'Período de Apuração\s*(.*)',
        'Principal': r'Principal\s*([\d.,]+)',
        'Selic Acumulada': r'Selic Acumulada\s*([\d.,]+)',
        'Crédito Atualizado': r'Crédito Atualizado\s*([\d.,]+)',
        'Saldo do Crédito Original': r'Saldo do Crédito Original\s*([\d.,]+)',
        'Valor Original do Crédito Inicial': r'Valor Original do Crédito Inicial\s*([\d.,]+)',
        '0001. Período de Apuração': r'0001\. Período de Apuração\s*(.*)',
        'Código da Receita/Denominação': r'Código da Receita/Denominação\s*(.*)',
        'Débito Controlado em Processo': r'Débito Controlado em Processo\s*(.*)',
        'Multa': r'Multa\s*([\d.,]+)',
        'Juros': r'Juros\s*([\d.,]+)',
        'Total': r'Total\s*([\d.,]+)'
    }

    dados_extraidos = {}

    for chave, padrao in regex_patterns.items():
        match = re.search(padrao, texto)
        dados_extraidos[chave] = match.group(1).strip() if match else None

    return dados_extraidos
