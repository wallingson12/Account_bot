import os
import pandas as pd
import pdfplumber
from pdf2image import convert_from_path
from ocr.ocr import process_image, extract_ocr_data_from_image, config_map
from .text_parser_dcomp import extrair_dados_texto_dcomp

def processar_dcomp(diretorio, usar_ocr=True, dpi=300):
    if not os.path.exists(diretorio):
        raise FileNotFoundError("O diretório especificado não foi encontrado.")

    all_data = []

    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(diretorio, arquivo)
            print(f"📄 Processando: {arquivo}")

            try:
                texto = ""

                if usar_ocr:
                    images = convert_from_path(caminho_pdf, dpi=dpi)
                    for i, img in enumerate(images, start=1):
                        print(f"🧠 OCR - Página {i}")
                        img = img.convert("RGB")
                        processed_img = process_image(img)  # ou qualquer pré-processamento
                        text_page, confidence = extract_ocr_data_from_image(processed_img, 'dcomp', config_map)
                        print(f"Confiança média da página {i}: {confidence:.2f}")
                        texto += "\n" + text_page
                else:
                    with pdfplumber.open(caminho_pdf) as pdf:
                        for i, page in enumerate(pdf.pages, start=1):
                            print(f"🖨️ Texto direto - Página {i}")
                            text_page = page.extract_text() or ""
                            texto += "\n" + text_page

                dados = extrair_dados_texto_dcomp(texto)
                dados['Número'] = arquivo
                dados['CRÉDITO'] = 'CRÉDITO PAGAMENTO INDEVIDO OU A MAIOR'

                all_data.append(dados)

            except Exception as e:
                print(f"❌ Erro ao processar {arquivo}: {e}")

    if not all_data:
        print("Nenhum dado extraído.")
        return pd.DataFrame()

    df = pd.DataFrame(all_data)
    caminho_saida = os.path.join(diretorio, "dcomp_extraido.xlsx")
    df.to_excel(caminho_saida, index=False)
    print(f"✅ Dados extraídos e salvos em '{caminho_saida}'")

    return df