import pandas as pd
import re

def clean_value(value):
    if value:
        value = re.sub(r'[^\d.,]', '', value)
        return value if value else '0,00'
    return '0,00'

def value_to_float(value):
    try:
        return float(value.replace('.', '').replace(',', '.'))
    except:
        return 0.0

def clean_description(description):
    return re.sub(r'[^A-Za-zÀ-ÿ0-9 ]', '', description).strip()

def clean_document_number(text):
    return re.sub(r'(\d{15,})/', r'\1', text)
