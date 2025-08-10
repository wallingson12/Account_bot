import os
import pandas as pd
from ocr.ocr import process_image, image_to_data_and_text
from .text_parser_dcomp import extrair_dados_texto_dcomp

def processar_dcomp(diretorio, usar_ocr=True):
    if not os.path.exists(diretorio):
        raise FileNotFoundError("O diretório especificado não foi encontrado.")

    all_data = []

    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(diretorio, arquivo)
            print(f"Processando: {arquivo}")

            texto = image_to_data_and_text(caminho_pdf, usar_ocr=usar_ocr)

            dados = extrair_dados_texto_dcomp(texto)
            dados['Número'] = arquivo
            dados['CRÉDITO'] = 'CRÉDITO PAGAMENTO INDEVIDO OU A MAIOR'

            all_data.append(dados)

    df = pd.DataFrame(all_data)
    caminho_saida = os.path.join(diretorio, "dcomp_extraido.xlsx")
    df.to_excel(caminho_saida, index=False)
    print(f"Dados extraídos e salvos em '{caminho_saida}'")

    return df
