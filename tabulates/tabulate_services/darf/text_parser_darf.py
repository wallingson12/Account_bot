import re
from tabulates.utils.darf_utils import *

def extract_cnpj_and_razao(text):
    cnpj_match = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', text)
    cnpj = cnpj_match.group(1) if cnpj_match else None

    razao_social = None
    if cnpj:
        cnpj_index = text.find(cnpj)
        linha_cnpj = text[cnpj_index:].splitlines()[0]
        razao_raw = linha_cnpj.replace(cnpj, '')
        razao_social = re.sub(r'[^A-Za-zÀ-ÿ0-9 .,]', '', razao_raw).strip()

    return cnpj, razao_social


def extract_collection_date(lines):
    for i, line in enumerate(lines):
        if "Data de Arrecadação" in line:
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                match_data = re.search(r'\d{2}/\d{2}/\d{4}', next_line)
                if match_data:
                    return match_data.group(0)
    return None


def create_record(filename, page_number, cnpj, razao_social, period_start, due_date, collection_date,
                  document_number, match, reserved_value):
    codigo = match[0]
    descricao = clean_description(match[1])
    principal = clean_value(match[2])
    multa = clean_value(match[3])
    juros = clean_value(match[4])
    total = clean_value(match[5])

    is_total = 'TOTAIS' in descricao.upper()

    if is_total:
        return None

    return {
        "Arquivo": filename,
        "Página": page_number,
        "CNPJ": cnpj,
        "Razão Social": razao_social,
        "Período Apuração": period_start,
        "Data de Vencimento": due_date,
        "Data de Arrecadação": collection_date,
        "Número de Documento": document_number,
        "Código": codigo,
        "Descrição": descricao,
        "Principal": principal,
        "Multa": multa,
        "Juros": juros,
        "Total": total,
        "Valor Reservado/Restituído": reserved_value
    }
