import gc
import pandas as pd
from tabulates.tabulate_services.recolhimentos.processor_recolhimentos import extrair_recolhimento_pdf


class RecolhimentosService:

    def processar(self, pasta_pdfs, usar_ocr=False):
        try:
            df = extrair_recolhimento_pdf(pasta_pdfs, usar_ocr=usar_ocr)
            gc.collect()
            return df
        except Exception as e:
            print(f"❌ Recolhimentos erro: {e}")
            return pd.DataFrame()