import os, gc
import pandas as pd
from tqdm import tqdm

from account_tools.utils.utils import listar_pdfs
from ocr.ocr import pdf_to_images, extract_ocr_data_from_image, config_map
from tabulates.tabulate_services.darf.processor_darf import extrair_infos_darf


class DarfService:

    def processar(self, pasta_pdfs, usar_ocr=True):
        registros = []

        for arquivo in listar_pdfs(pasta_pdfs):
            caminho = os.path.join(pasta_pdfs, arquivo)
            print(f"[DARF] {arquivo}")

            try:
                if usar_ocr:
                    imagens = pdf_to_images(caminho, dpi=500)
                    for img in tqdm(imagens):
                        extract_ocr_data_from_image(img, "darf", config_map)
                        del img

                dados = extrair_infos_darf(caminho, arquivo)
                for d in dados or []:
                    d["ARQUIVO_ORIGEM"] = arquivo
                    registros.append(d)

            except Exception as e:
                print(f"❌ DARF erro {arquivo}: {e}")
            finally:
                gc.collect()

        if not registros:
            return pd.DataFrame()

        df = pd.DataFrame(registros)
        df.to_excel(os.path.join(pasta_pdfs, "DARF_Consolidado.xlsx"), index=False)
        return df