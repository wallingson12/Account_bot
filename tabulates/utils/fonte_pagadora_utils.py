import re

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def clean_cnpj(cnpj):
    return re.sub(r'[^\d]', '', cnpj)

def filter_name(name):
    return re.sub(r'[^A-Z\s]', '', name).strip()
