import os, gc
import pandas as pd
from pathlib import Path

from ocr.ocr import pdf_to_images, extract_ocr_data_from_image, preprocess_cfop_image, config_map
from tabulates.tabulate_services.cfop.text_parser_cfop import extrair_cfop_valores


class CfopService:

    def processar(self, pasta_pdfs, usar_ocr=True):
        registros = []

        for pdf in Path(pasta_pdfs).glob("*.pdf"):
            imagens = pdf_to_images(pdf)

            for i, img in enumerate(imagens, 1):
                img = preprocess_cfop_image(img.convert("RGB"))
                texto, _ = extract_ocr_data_from_image(img, "cfop", config_map)
                registros.extend(extrair_cfop_valores(texto, pdf.name, i))
                del img

            gc.collect()

        df = pd.DataFrame(registros)
        if not df.empty:
            df.to_excel(os.path.join(pasta_pdfs, "CFOP_Consolidado.xlsx"), index=False)
        return df
