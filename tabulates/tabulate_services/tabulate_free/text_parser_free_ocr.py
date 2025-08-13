import re
from ocr.ocr import config_map

def parse_text_free(imagens, tipo):
    all_rows = []

    if tipo not in config_map:
        raise ValueError(f"O tipo '{tipo}' não está definido no config_map.")

    preprocess = config_map[tipo]['preprocess']
    ocr_func = config_map[tipo]['ocr']

    for img in imagens:
        img_preprocessada = preprocess(img)
        _, texto = ocr_func(img_preprocessada)

        linhas = [l.strip() for l in texto.splitlines() if l.strip()]

        conta = next((l.replace("Conta:", "").strip() for l in linhas if l.upper().startswith("CONTA:")), "")
        saldo_anterior = ""
        for l in linhas:
            if "SALDO ANTERIOR" in l.upper():
                match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})", l)
                if match:
                    saldo_anterior = match.group(1)
                    break

        rows, linha_atual = [], None

        for l in linhas:
            match = re.match(
                r"^(\d{2}/\d{2}/\d{4})\s+(\d+)\s+(.+?)\s+(\d+)\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2}[CD]?)$",
                l)

            if match:
                linha_atual = list(match.groups())
                rows.append(linha_atual)
            elif linha_atual:
                extra = re.sub(r'\b\d{1,3}(?:\.\d{3})*,\d{2}[CD]?\b', '', l).strip()
                extra = re.sub(r'^\d{2}/\d{2}/\d{4}', '', extra).strip()
                if extra:
                    linha_atual[2] += ' ' + extra

        for r in rows:
            r.append(conta)
            r.append(saldo_anterior)

        all_rows.extend(rows)

    return all_rows