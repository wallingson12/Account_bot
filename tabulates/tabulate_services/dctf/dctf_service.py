import os, gc
import pandas as pd

from account_tools.utils.utils import listar_pdfs
from tabulates.tabulate_services.dctf.dctf_processor import extrair_dctf_pdf


class DctfService:

    def processar(self, pasta_pdfs, usar_ocr=True):
        consolidado = []

        for arquivo in listar_pdfs(pasta_pdfs):
            caminho = os.path.join(pasta_pdfs, arquivo)
            print(f"[DCTF] {arquivo}")

            try:
                df, _ = extrair_dctf_pdf(caminho, usar_ocr)
                df["ARQUIVO_ORIGEM"] = arquivo
                consolidado.append(df)
            except Exception as e:
                print(f"❌ DCTF erro {arquivo}: {e}")
            finally:
                gc.collect()

        if not consolidado:
            return pd.DataFrame()

        final = pd.concat(consolidado, ignore_index=True)
        final.to_excel(os.path.join(pasta_pdfs, "DCTF_Consolidado.xlsx"), index=False)
        return final
