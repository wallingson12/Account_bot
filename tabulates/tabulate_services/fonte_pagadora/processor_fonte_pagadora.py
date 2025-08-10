import os
from ocr.ocr import preprocess_ocr_fonte_pagadora_image, image_to_data_and_text
from text_parser_fonte_pagadora  import find_full_patterns
from gerar_excel.gerar_excel import save_to_excel
import pandas as pd

def process_pdfs_in_folder(pdf_folder, excel_path, use_ocr=False):
    arquivos_pdf = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    consolidado_df = pd.DataFrame()

    for arquivo_pdf in arquivos_pdf:
        caminho_pdf = os.path.join(pdf_folder, arquivo_pdf)
        print(f"Processando: {arquivo_pdf}")

        try:
            if use_ocr:
                texto = preprocess_ocr_fonte_pagadora_image(caminho_pdf)
            else:
                texto = image_to_data_and_text(caminho_pdf)

            dados = find_full_patterns(texto)
            df = pd.DataFrame(dados, columns=['CNPJ', 'Nome', 'Data', 'Código', 'Rendimento', 'Imposto'])
            df['Arquivo_Origem'] = arquivo_pdf

            consolidado_df = pd.concat([consolidado_df, df], ignore_index=True)

        except Exception as e:
            print(f"Erro ao processar {arquivo_pdf}: {e}")

    save_to_excel(consolidado_df, excel_path)
    print(f"\n✅ Consolidado salvo em: {excel_path}")

# if __name__ == "__main__":
#     pasta_pdfs = r"C:\Users\wallingson.silva\Desktop\WALLINGSON\TO DO\Aplicação_tabulacao\files\FONTES PAGADORAS"
#     excel_saida = r"C:\Users\wallingson.silva\Desktop\WALLINGSON\TO DO\Aplicação_tabulacao\files\FONTES PAGADORAS\consolidado.xlsx"
#     process_pdfs_in_folder(pasta_pdfs, excel_saida, use_ocr=True)  # ou False para sem OCR
