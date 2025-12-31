from account_tools.utils.decorators import log_de_erro
from services.consultar_cnpj.consult_cnpj import consulta_cnpj


class CnpjService:

    @log_de_erro
    def consultar(
        self,
        taxa_consulta=3,
        arquivo_entrada="cnpjs.xlsx",
        arquivo_saida="resultado_cnpjs.xlsx"
    ):
        return consulta_cnpj(
            taxa_consulta=taxa_consulta,
            arquivo_entrada=arquivo_entrada,
            arquivo_saida=arquivo_saida
        )