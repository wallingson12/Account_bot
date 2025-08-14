import re

def extrair_cfop_valores(texto, nome_arquivo, pagina):
    registros = []
    cfop_pattern = re.compile(r"\b(\d{4})\b")
    valor_pattern = re.compile(r"\d{1,3}(?:\.\d{3})*,\d{2}")
    data_pattern = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")

    for linha in texto.splitlines():
        linha = linha.strip()
        if data_pattern.search(linha):
            continue  # ignora linha com data
        cfop_match = cfop_pattern.search(linha)
        valor_matches = valor_pattern.findall(linha)
        if cfop_match and valor_matches:
            cfop = cfop_match.group(1)
            valores = valor_matches[:5] + [''] * (5 - len(valor_matches))
            vlc, base, imp, isentas, outras = valores
            registros.append({
                'Arquivo': nome_arquivo,
                'Página': pagina,
                'CFOP': cfop,
                'VL.C': vlc,
                'BASE': base,
                'IMP': imp,
                'ISENTAS': isentas,
                'OUTRAS': outras
            })
    return registros
