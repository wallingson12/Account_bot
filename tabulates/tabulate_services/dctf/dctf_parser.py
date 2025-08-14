import re
import pandas as pd
import sys
import os
from tabulates.utils.dctf_utils import limpar_valor

def parse_text_dctf(text, dctf_detalhamento, grupo_atual, novo_grupo, soma_principal, soma_multas, soma_juros):
    padrao_detalhamento = {
        "GRUPO DO TRIBUTO": r'GRUPO DO TRIBUTO\s*:?\s*(.+)',
        "CÓDIGO RECEITA": r'CÓDIGO RECEITA\s*:\s*(.+)',
        "PERIODICIDADE": r'PERIODICIDADE\s*:\s*(\S+)',
        "PA": r'PA:\s*(\d{2}/\d{2}/\d{4})',
        "DÉBITO APURADO": r'DÉBITO APURADO\s*:?[\s]*([\d.,/]+)',
        "PAGAMENTO": r'PAGAMENTO\s*:?[\s]*([\d.,/]+)',
        "COMPENSAÇÕES": r'COMPENSAÇÕES\s*:?[\s]*([\d.,/]+)',
        "SUSPENSÃO": r'SUSPENSÃO\s*:?[\s]*([\d.,/]+)',
        "SOMA DOS CRÉDITOS VINCULADOS": r'SOMA DOS CRÉDITOS VINCULADOS\s*:\s*([\d.,/]+)',
        "Valor do Principal": r'Valor do Principal\s*:\s*([\d.,/]+)',
        "Valor da Multa": r'Valor da Multa\s*:?[\s]*([\d.,/]+)',
        "Valor dos Juros": r'Valor dos Juros\s*:?[\s]*([\d.,/]+)',
        "Valor Pago do Débito": r'Valor Pago do D[êéEe]{1,2}bito\s*:\s*([\d.,/]+)',
        "Valor Total do DARF": r"Valor Total do DARF[^0-9]{0,10}([\d.,]+)"
    }

    for chave, padrao in padrao_detalhamento.items():
        match = re.search(padrao, text)
        if match:
            valor = match.group(1).strip()

            if chave == "GRUPO DO TRIBUTO":
                # Correção para casos com abreviação ou OCR ruim
                if "PATRIM" in valor.upper():
                    valor = "PIS/PASEP - CONTRIB. P/PROGRAMA DE INTEGRAÇÃO SOCIAL/FORMAÇÃO PATRIM. SERV. PÚBLICO"

                if grupo_atual != valor:
                    if not novo_grupo:
                        dctf_detalhamento["Valor do Principal"].append(soma_principal)
                        dctf_detalhamento["Valor da Multa"].append(soma_multas)
                        dctf_detalhamento["Valor dos Juros"].append(soma_juros)
                        soma_principal = 0
                        soma_multas = 0
                        soma_juros = 0

                    grupo_atual = valor
                    novo_grupo = False

                dctf_detalhamento[chave].append(valor)

            elif chave == "Valor do Principal":
                soma_principal += float(limpar_valor(valor).replace(',', '.'))

            elif chave == "Valor da Multa":
                soma_multas += float(limpar_valor(valor).replace(',', '.'))

            elif chave == "Valor dos Juros":
                soma_juros += float(limpar_valor(valor).replace(',', '.'))

            else:
                dctf_detalhamento[chave].append(valor)

        else:
            # Evita append duplicado para campos acumulados
            if chave not in ["Valor do Principal", "Valor da Multa", "Valor dos Juros"]:
                dctf_detalhamento[chave].append(None)

    return dctf_detalhamento, grupo_atual, novo_grupo, soma_principal, soma_multas, soma_juros
