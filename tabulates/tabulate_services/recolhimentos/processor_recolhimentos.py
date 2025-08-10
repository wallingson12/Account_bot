import os
import re
import pandas as pd
import camelot
from ocr.ocr import process_image, image_to_data_and_text

# Regex de linha mantido aqui, pois faz parte da responsabilidade desse módulo
PADRAO_LINHA = r'(?P<DARF>[^\s]+|\bDARF\s+\d+)\s+' \
               r'(?P<Data_de_arreacadação>\d{2}/\d{2}/\d{4})\s+' \
               r'(?P<Data_de_vencimento>\d{2}/\d{2}/\d{4})\s+' \
               r'(?P<Periodo_de_apuração>\d{2}/\d{2}/\d{4})\s+' \
               r'(?P<Código_da_receita>[\w]{4})\s+' \
               r'(?P<Número_de_documento>\d{10,17})\s+' \
               r'(?P<Valor>[0-9.,]+)'

def extrair_recolhimento_pdf(diretorio, usar_ocr=False):
    if not os.path.exists(diretorio):
        raise FileNotFoundError("O diretório especificado não foi encontrado.")

    dados_totais = []

    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(diretorio, arquivo)

            if usar_ocr:
                dados_totais.extend(image_to_data_and_text(caminho_pdf, PADRAO_LINHA))
            else:
                tabelas = camelot.read_pdf(caminho_pdf, pages='all', flavor='stream')
                for tabela in tabelas:
                    for _, linha in tabela.df.iterrows():
                        texto = ' '.join(linha.values)
                        match = re.match(PADRAO_LINHA, texto)
                        if match:
                            dados_totais.append(match.groupdict())

    return pd.DataFrame(dados_totais)