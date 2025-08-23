import pandas as pd
import re

# Aceita: "123,45", "1.234,56", "0,00", "12.345.678,90"
MONEY_PATTERN = re.compile(r'^\d{1,3}(?:\.\d{3})*,\d{2}$')

def clean_value(value):
    """
    Normaliza valores monetários no formato brasileiro.
    - Se não for válido, retorna "0,00"
    - Sempre retorna string no formato "X.XXX,XX"
    """
    if not value:
        return "0,00"

    # mantém apenas dígitos, ponto e vírgula
    v = re.sub(r'[^\d.,]', '', str(value))

    # precisa ter vírgula e estar no formato correto
    if not v or ',' not in v or not MONEY_PATTERN.match(v):
        return "0,00"

    # tenta converter para float
    try:
        val_float = float(v.replace('.', '').replace(',', '.'))
    except ValueError:
        return "0,00"

    # formata de volta no padrão BR
    return f"{val_float:,.2f}".replace(".", ",")

def value_to_float(value):
    """
    Converte valor monetário BR para float.
    - Usa sempre clean_value antes para garantir consistência.
    """
    try:
        clean = clean_value(value)
        return float(clean.replace('.', '').replace(',', '.'))
    except:
        return 0.0

def clean_description(description):
    """
    Limpa descrição, mantendo apenas letras, números e espaços.
    """
    return re.sub(r'[^A-Za-zÀ-ÿ0-9 ]', '', str(description)).strip()

def clean_document_number(text):
    """
    Ajusta número de documento, removendo a barra após sequência longa de dígitos.
    """
    return re.sub(r'(\d{15,})/', r'\1', str(text))
