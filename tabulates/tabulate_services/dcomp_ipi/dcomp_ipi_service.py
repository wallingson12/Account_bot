import gc
import pandas as pd
from tabulates.tabulate_services.dcomp_ipi.processor_dcomp_ipi import processor_dcomp_ipi


class DcompIpiService:

    def processar(self, pasta_pdfs, usar_ocr=False):
        try:
            df = processor_dcomp_ipi(pasta_pdfs, usar_ocr)
            gc.collect()
            return df
        except Exception as e:
            print(f"❌ DCOMP IPI erro: {e}")
            return pd.DataFrame()
