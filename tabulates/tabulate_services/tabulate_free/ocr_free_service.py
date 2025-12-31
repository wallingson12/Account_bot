import os, gc
import pandas as pd

from account_tools.utils.utils import listar_pdfs
from ocr.ocr import pdf_to_images, extract_ocr_data_from_image, config_map
from tabulates.tabulate_services.tabulate_free.text_parser_free_ocr import parse_text_free


class OcrFreeService:

    def processar(self, pasta_pdfs, usar_ocr=True):
        linhas = []

        for arquivo in listar_pdfs(pasta_pdfs):
            imagens = pdf_to_images(os.path.join(pasta_pdfs, arquivo))

            for img in imagens:
                texto, _ = extract_ocr_data_from_image(img, "free_tabulate", config_map)
                linhas.extend(parse_text_free(texto))
                del img

            gc.collect()

        df = pd.DataFrame(
            linhas,
            columns=["Data","Numero","Descricao","Quantidade","Valor","DC","Conta","Saldo"]
        )

        if not df.empty:
            df.to_excel(os.path.join(pasta_pdfs, "OCR_Free.xlsx"), index=False)
        return df
