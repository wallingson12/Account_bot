import gc
import pandas as pd
from tabulates.tabulate_services.dcomp.processor_dcomp import processar_dcomp


class DcompService:

    def processar(self, pasta_pdfs, usar_ocr=True):
        try:
            df = processar_dcomp(pasta_pdfs, usar_ocr)
            gc.collect()
            return df
        except Exception as e:
            print(f"❌ DCOMP erro: {e}")
            return pd.DataFrame()
