import os
import pandas as pd
from pdf2image import convert_from_path
from ocr.ocr import preprocess_dctf_image, extract_ocr_data_from_image, config_map
from .dctf_parser import  parse_text_dctf
from pdf2image import convert_from_path
import pdfplumber

def extrair_dctf_pdf(caminho_pdf, usar_ocr=True, nome_saida_detalhamento='dctf_detalhamento.xlsx', dpi=600):
    """
    Extrai dados da DCTF a partir de um PDF.

    Args:
        caminho_pdf (str): caminho para o arquivo PDF.
        usar_ocr (bool): se True, usa OCR para extrair texto da imagem.
        nome_saida_detalhamento (str): nome do arquivo Excel de saída.
        dpi (int): resolução para converter PDF em imagem.

    Returns:
        pd.DataFrame: DataFrame com os detalhes extraídos.
        list[str]: lista com textos extraídos de cada página/processamento.
    """

    padrao_detalhamento = {
        "GRUPO DO TRIBUTO": [],
        "CÓDIGO RECEITA": [],
        "PERIODICIDADE": [],
        "PA": [],
        "DÉBITO APURADO": [],
        "PAGAMENTO": [],
        "COMPENSAÇÕES": [],
        "SUSPENSÃO": [],
        "SOMA DOS CRÉDITOS VINCULADOS": [],
        "Valor do Principal": [],
        "Valor da Multa": [],
        "Valor dos Juros": [],
        "Valor Pago do Débito": [],
        "Valor Total do DARF": []
    }

    dctf_detalhamento = {k: [] for k in padrao_detalhamento}
    all_texts = []
    soma_principal = 0
    soma_multas = 0
    soma_juros = 0
    novo_grupo = True
    grupo_atual = None

    if usar_ocr:
        images = convert_from_path(caminho_pdf, dpi=dpi, first_page=3)
        for img in images:
            img = img.convert('RGB')
            processed_img = preprocess_dctf_image(img)
            text, confidence = extract_ocr_data_from_image(processed_img, 'dctf', config_map)
            print(f"OCR confidence média: {confidence:.2f}")
            print(text)
            all_texts.append(text)

            dctf_detalhamento, grupo_atual, novo_grupo, soma_principal, soma_multas, soma_juros = parse_text_dctf(
                text, dctf_detalhamento, grupo_atual, novo_grupo, soma_principal, soma_multas, soma_juros)
    else:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages[2:]:  # começa da página 3 (índice 2)
                text = pagina.extract_text() or ""
                all_texts.append(text)
                print(text)

                dctf_detalhamento, grupo_atual, novo_grupo, soma_principal, soma_multas, soma_juros = parse_text_dctf(
                    text, dctf_detalhamento, grupo_atual, novo_grupo, soma_principal, soma_multas, soma_juros)

    if not novo_grupo:
        dctf_detalhamento["Valor do Principal"].append(soma_principal)
        dctf_detalhamento["Valor da Multa"].append(soma_multas)
        dctf_detalhamento["Valor dos Juros"].append(soma_juros)

    max_len_detalhamento = max(len(v) for v in dctf_detalhamento.values())

    dctf_detalhamento_df = pd.DataFrame({
        k: (v + [None] * (max_len_detalhamento - len(v))) for k, v in dctf_detalhamento.items()
    })

    dctf_detalhamento_df.to_excel(nome_saida_detalhamento, index=False)

    return dctf_detalhamento_df, all_texts