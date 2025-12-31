from account_tools.utils.decorators import log_de_erro
from services.limpar_pasta.limpar_pasta import limpar_arquivos_por_formato
from services.organizador_por_idetificador.organizador_por_idetificador import mover_arquivos_por_extensao


class FileService:

    @log_de_erro
    def limpar_por_formato(self, pasta, manter):
        return limpar_arquivos_por_formato(pasta, manter)

    @log_de_erro
    def mover_por_extensao(self, origem, destino, extensao):
        return mover_arquivos_por_extensao(origem, destino, extensao)