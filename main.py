import pytesseract
from config.config import caminho_tesseract

# ===== Services =====
from services.excel_service import ExcelService
from services.file_service import FileService
from services.xml_service import XmlService
from services.cnpj_service import CnpjService
from services.ipi_service import IPIService
from services.divisor_pdf.divisor_pdf import dividir_pdf

# ===== Tabuladores =====
from tabulates.tabulate_services.dctf.dctf_service import DctfService
from tabulates.tabulate_services.darf.darf_service import DarfService
from tabulates.tabulate_services.fonte_pagadora.fonte_pagadora_service import FontePagadoraService
from tabulates.tabulate_services.cfop.cfop_service import CfopService
from tabulates.tabulate_services.dcomp.dcomp_service import DcompService
from tabulates.tabulate_services.dcomp_ipi.dcomp_ipi_service import DcompIpiService
from tabulates.tabulate_services.recolhimentos.recolhimentos_service import RecolhimentosService
from tabulates.tabulate_services.tabulate_free.ocr_free_service import OcrFreeService


class Contador:
    """
    Classe central que integra todos os serviços do sistema.
    Permite manipulação de Excel, arquivos, XMLs, CNPJs, PDFs, IPI e tabuladores específicos.
    """

    def __init__(self):
        # Configura o caminho do executável do Tesseract OCR
        pytesseract.pytesseract.tesseract_cmd = caminho_tesseract

        # Inicializa serviços base
        self.excel = ExcelService()        # Processamento de planilhas Excel
        self.files = FileService()         # Manipulação de arquivos (mover, limpar, etc.)
        self.xml = XmlService()            # Processamento e organização de arquivos XML
        self.cnpj = CnpjService()          # Consulta de CNPJs via API
        self.ipi = IPIService()            # Rotinas de IPI (R11, R12, R13, R15, R21)

        # Inicializa tabuladores específicos
        self.dctf_tab = DctfService()                  # Tabulador DCTF
        self.darf_tab = DarfService()                  # Tabulador DARF
        self.fontes_tab = FontePagadoraService()       # Tabulador fontes pagadoras
        self.cfop_tab = CfopService()                  # Tabulador CFOP
        self.dcomp_tab = DcompService()                # Tabulador DCOMP
        self.dcomp_ipi_tab = DcompIpiService()        # Tabulador DCOMP IPI
        self.recolhimentos_tab = RecolhimentosService()  # Tabulador recolhimentos
        self.ocr_livre_tab = OcrFreeService()         # Tabulador OCR livre

    # ===== EXCEL =====
    def comparar_excel(self,caminho_excel_origem,aba_origem,linhas_pular_origem,
        caminho_excel_destino,aba_destino,linhas_pular_destino,colunas_chave_origem,
        colunas_chave_destino,diretorio_saida):
        """
        Compara e classifica dois arquivos Excel utilizando chaves compostas.
        Retorna o resultado classificado (Correto, Excluir, Estudar, Incluir).
        """
        return self.excel.conciliar(
            caminho_excel_origem, aba_origem, linhas_pular_origem,
            caminho_excel_destino, aba_destino, linhas_pular_destino,
            colunas_chave_origem, colunas_chave_destino,
            diretorio_saida
        )

    def dividir_excel(self, arquivo_excel, coluna_divisao, diretorio_output):
        """
        Divide um arquivo Excel em vários arquivos, um para cada valor único
        da coluna especificada.
        """
        return self.excel.dividir(
            arquivo_excel=arquivo_excel,
            coluna_divisao=coluna_divisao,
            diretorio_output=diretorio_output
        )

    def unificar_excel(self, pasta):
        """
        Unifica todos os arquivos Excel dentro de uma pasta em um único arquivo.
        """
        return self.excel.unificar(pasta)

    # ===== FILES =====
    def limpar_pasta(self, pasta_raiz, formato_manter):
        """
        Limpa todos os arquivos de uma pasta, mantendo apenas os formatos especificados.
        """
        return self.files.limpar_por_formato(
            pasta_raiz=pasta_raiz,
            formato_manter=formato_manter
        )

    def mover_extensao(self, diretorio_raiz, pasta_output, extensao):
        """
        Move arquivos de um tipo específico (extensão) para outra pasta.
        """
        return self.files.mover_por_extensao(
            diretorio_raiz=diretorio_raiz,
            pasta_output=pasta_output,
            extensao=extensao
        )

    # ===== XML =====
    def mover_esocial(self, diretorio_origem, diretorio_destino):
        """
        Move arquivos eSocial de uma pasta para outra.
        """
        return self.xml.mover_esocial(
            diretorio_origem=diretorio_origem,
            diretorio_destino=diretorio_destino
        )

    def organizar_xml(self, origem, destino, tipo):
        """
        Organiza arquivos XML por data ou outro critério definido.
        """
        return self.xml.organizar_por_data(
            origem=origem,
            destino=destino,
            tipo=tipo
        )

    # ===== CNPJ =====
    def consultar_cnpj(self, taxa_consulta=3, arquivo_entrada=None, arquivo_saida=None):
        """
        Consulta uma lista de CNPJs em arquivo Excel.
        Controla taxa de consulta por minuto para evitar bloqueio da API.
        """
        kwargs = {"taxa_consulta": taxa_consulta}

        if isinstance(arquivo_entrada, str) and arquivo_entrada.strip():
            kwargs["arquivo_entrada"] = arquivo_entrada
        if isinstance(arquivo_saida, str) and arquivo_saida.strip():
            kwargs["arquivo_saida"] = arquivo_saida

        return self.cnpj.consultar(**kwargs)

    # ===== PDF =====
    def dividir_pdf(self, pdf_path):
        """
        Divide um PDF em múltiplos arquivos (por páginas ou critérios internos).
        """
        return dividir_pdf(pdf_path)

    # ===== TABULADORES =====
    def dctf(self, pasta_pdfs, usar_ocr=True):
        """
        Processa PDFs para o tabulador DCTF.
        """
        return self.dctf_tab.processar(pasta_pdfs, usar_ocr)

    def darf(self, pasta_pdfs, usar_ocr=True):
        """
        Processa PDFs para o tabulador DARF.
        """
        return self.darf_tab.processar(pasta_pdfs, usar_ocr)

    def fontes(self, pasta_pdfs, usar_ocr=True):
        """
        Processa PDFs para o tabulador de fontes pagadoras.
        """
        return self.fontes_tab.processar(pasta_pdfs, usar_ocr)

    def cfop(self, pasta_pdfs, usar_ocr=True):
        """
        Processa PDFs para o tabulador CFOP.
        """
        return self.cfop_tab.processar(pasta_pdfs, usar_ocr)

    def dcomp(self, pasta_pdfs, usar_ocr=True):
        """
        Processa PDFs para o tabulador DCOMP.
        """
        return self.dcomp_tab.processar(pasta_pdfs, usar_ocr)

    def dcomp_ipi(self, pasta_pdfs, usar_ocr=False):
        """
        Processa PDFs para o tabulador DCOMP IPI.
        Por padrão, OCR não é usado.
        """
        return self.dcomp_ipi_tab.processar(pasta_pdfs, usar_ocr)

    def recolhimentos(self, pasta_pdfs, usar_ocr=False):
        """
        Processa PDFs para o tabulador de recolhimentos.
        """
        return self.recolhimentos_tab.processar(pasta_pdfs, usar_ocr)

    def ocr_livre(self, pasta_pdfs):
        """
        Processa PDFs com OCR livre, sem tabulador específico.
        """
        return self.ocr_livre_tab.processar(pasta_pdfs)

    # ===== IPI =====
    def r11_r12(self, arquivo_excel, diretorio_saida):
        """
        Processa arquivos Excel para gerar txt de importação para o registro do  tipo R11/R12.
        """
        return self.ipi.r11_r12(arquivo_excel, diretorio_saida)

    def r13(self, arquivo_excel, diretorio_saida):
        """
        Processa arquivos Excel para gerar txt de importação para o registro do  tipo R13.
        """
        return self.ipi.r13(arquivo_excel, diretorio_saida)

    def r15(self, arquivo_excel, diretorio_saida):
        """
        Processa arquivos Excel para gerar txt de importação para o registro do  tipo R15.
        """
        return self.ipi.r15(arquivo_excel, diretorio_saida)

    def r21(self, arquivo_excel, diretorio_saida):
        """
        Processa arquivos Excel para gerar txt de importação para o registro do  tipo R21.
        """
        return self.ipi.r21(arquivo_excel, diretorio_saida)
