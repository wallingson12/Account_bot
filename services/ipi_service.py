from account_tools.utils.decorators import log_de_erro
from dcomp_file.generator import RegistroIPI


class IPIService:

    def __init__(self):
        self.gerador = RegistroIPI()

    @log_de_erro
    def r11_r12(self, arquivo, saida):
        return self.gerador.processar_r11_r12(arquivo, saida)

    @log_de_erro
    def r13(self, arquivo, saida):
        return self.gerador.processar_r13(arquivo, saida)

    @log_de_erro
    def r15(self, arquivo, saida):
        return self.gerador.processar_r15(arquivo, saida)

    @log_de_erro
    def r21(self, arquivo, saida):
        return self.gerador.processar_r21(arquivo, saida)