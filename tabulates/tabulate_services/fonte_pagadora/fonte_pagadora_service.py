import os, gc
import pandas as pd

from account_tools.utils.utils import listar_pdfs
from ocr.ocr import pdf_to_images, extract_ocr_data_from_image, config_map
from tabulates.tabulate_services.fonte_pagadora.text_parser_fonte_pagadora import find_full_patterns


class FontePagadoraService:

    def processar(self, pasta_pdfs, usar_ocr=True):
        dados_finais = []

        if not usar_ocr:
            return pd.DataFrame()

        for arquivo in listar_pdfs(pasta_pdfs):
            caminho = os.path.join(pasta_pdfs, arquivo)
            print(f"[FONTES] {arquivo}")

            try:
                imagens = pdf_to_images(caminho)
                textos = [
                    extract_ocr_data_from_image(img, "fonte_pagadora", config_map)[0]
                    for img in imagens
                ]
                texto = "\n".join(textos)

                dados = find_full_patterns(texto)
                for d in dados or []:
                    dados_finais.append({
                        "CNPJ": d[0],
                        "Nome": d[1],
                        "Data": d[2],
                        "Codigo": d[3],
                        "Rendimento": d[4],
                        "Imposto": d[5],
                        "ARQUIVO_ORIGEM": arquivo
                    })

            except Exception as e:
                print(f"❌ FONTES erro {arquivo}: {e}")
            finally:
                gc.collect()

        df = pd.DataFrame(dados_finais)
        if not df.empty:
            df.to_excel(os.path.join(pasta_pdfs, "Fontes_Pagadoras.xlsx"), index=False)
        return df
