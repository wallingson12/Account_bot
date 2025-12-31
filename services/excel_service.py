from account_tools.utils.decorators import log_de_erro
from services.comparador.comparador import classificar_conciliacao_excel
from services.dividir_excel.dividir_excel import dividir_planilha_por_coluna
from services.unificar_excel.unificar_excel import unificar_excel_da_pasta


class ExcelService:

    @log_de_erro
    def conciliar(self, *args, **kwargs):
        return classificar_conciliacao_excel(*args, **kwargs)

    @log_de_erro
    def dividir(self, arquivo, coluna, diretorio_output):
        return dividir_planilha_por_coluna(arquivo, coluna, diretorio_output)

    @log_de_erro
    def unificar(self, pasta):
        return unificar_excel_da_pasta(pasta)