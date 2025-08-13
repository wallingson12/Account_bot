import os
import pandas as pd
import pdfplumber
from pdf2image import convert_from_path

from account_tools.utils.utils import save_to_excel
from ocr.ocr import preprocess_ocr_fonte_pagadora_image, extract_ocr_data_from_image, config_map
from text_parser_fonte_pagadora import find_full_patterns

def process_pdfs_in_folder(pdf_folder, excel_path, use_ocr=False, dpi=300):
    arquivos_pdf = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    consolidado_df = pd.DataFrame()

    for arquivo_pdf in arquivos_pdf:
        caminho_pdf = os.path.join(pdf_folder, arquivo_pdf)
        print(f"📄 Processando: {arquivo_pdf}")

        try:
            texto = ""

            if use_ocr:
                images = convert_from_path(caminho_pdf, dpi=dpi)
                for i, img in enumerate(images, start=1):
                    print(f"🧠 OCR - Página {i}")
                    img = img.convert("RGB")
                    processed_img = preprocess_ocr_fonte_pagadora_image(img)
                    texto_ocr, confidence = extract_ocr_data_from_image(processed_img, 'fonte_pagadora', config_map)
                    print(f"Confiança média da página {i}: {confidence:.2f}")
                    texto += "\n" + texto_ocr
            else:
                with pdfplumber.open(caminho_pdf) as pdf:
                    for i, page in enumerate(pdf.pages, start=1):
                        print(f"🖨️ Texto direto - Página {i}")
                        texto += "\n" + (page.extract_text() or "")

            dados = find_full_patterns(texto)
            df = pd.DataFrame(dados, columns=['CNPJ', 'Nome', 'Data', 'Código', 'Rendimento', 'Imposto'])
            df['Arquivo_Origem'] = arquivo_pdf

            consolidado_df = pd.concat([consolidado_df, df], ignore_index=True)

        except Exception as e:
            print(f"❌ Erro ao processar {arquivo_pdf}: {e}")

    save_to_excel(consolidado_df, excel_path)
    print(f"\n✅ Consolidado salvo em: {excel_path}")
