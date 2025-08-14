import re
from tabulates.utils.fonte_pagadora_utils import clean_cnpj, filter_name

def find_full_patterns(text):
    cnpj_pattern = re.compile(r'\b(\d{2}[.,\s]?\d{3}[.,\s]?\d{3}[./\s]{1,2}?\d{4}[-\s]?\d{2})\b')
    date_pattern = re.compile(r'(\d{2}/\d{2}/\d{4})')
    # Exclui anos 2023-2026 para não confundir com código
    code_value_pattern = re.compile(r'\b(?!202[3-6])(\d{4})\b\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})')

    lines = text.split('\n')
    results = []

    cnpj, name, date = None, '', None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        cnpj_match = cnpj_pattern.search(line)
        if cnpj_match:
            cnpj = clean_cnpj(cnpj_match.group(1))
            name_part = line[cnpj_match.end():].strip()

            date_match = date_pattern.search(name_part)
            if date_match:
                date = date_match.group(1)
                name = filter_name(name_part[:date_match.start()].strip())
            else:
                name = filter_name(name_part)
            continue

        if cnpj and name and date:
            code_value_match = code_value_pattern.search(line)
            if code_value_match:
                code, rendimento, imposto = code_value_match.groups()
                results.append((cnpj, name, date, code, rendimento, imposto))

    return results
