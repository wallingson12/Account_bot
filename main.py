from services.comparador import comparar_e_classificar_excel
from services.consult_cnpj import consulta_cnpj
from services.dividir_excel import dividir_planilha_por_coluna
from services.limpar_pasta import limpar_arquivos_por_formato
from services.mover_arquivos_esocial import (
    mover_arquivos_xml_metade,
    organizar_xml_por_data,
)
from services.mover_arquivos_por_extensao import mover_arquivos_por_extensao
from services.unificar_excel import unificar_excel_da_pasta
from services.divisor_pdf import dividir_pdf
from account_tools.utils.decorators import log_de_erro

import os
import pandas as pd
from pathlib import Path
import pytesseract
from config.config import caminho_tesseract

from ocr.ocr import pdf_to_images, extract_ocr_data_from_image, config_map, preprocess_cfop_image
from tabulates.tabulate_services.dctf.dctf_processor import extrair_dctf_pdf
from tabulates.tabulate_services.fonte_pagadora.text_parser_fonte_pagadora import find_full_patterns
from tabulates.tabulate_services.darf.processor_darf import extrair_infos_darf
from tabulates.tabulate_services.tabulate_free.text_parser_free_ocr import parse_text_free
from tabulates.tabulate_services.CFOP.text_parser_cfop import extrair_cfop_valores
from tabulates.tabulate_services.dcomp.processor_dcomp import processar_dcomp
from tabulates.tabulate_services.dcomp_ipi.processor_dcomp_ipi import processor_dcomp_ipi
from tabulates.tabulate_services.recolhimentos.processor_recolhimentos import extrair_recolhimento_pdf
from tqdm import tqdm
import gc

from dcomp_file.generator import RegistroIPI

# Flags para ativar/desativar cada tipo de processamento
PROCESSAR_DCTF = False
PROCESSAR_FONTES = False
PROCESSAR_DARF = False
PROCESSAR_OCR_FREE = False
PROCESSAR_CFOP = False
PROCESSAR_DCOMP = False
PROCESSAR_DCOMP_IPI = False
PROCESSAR_RECOLHIMENTOS = False


def listar_pdfs(pasta_pdfs):
    pasta = Path(pasta_pdfs)
    return [f for f in os.listdir(pasta_pdfs) if f.lower().endswith('.pdf')]


class Contador:
    def __init__(self, caminho_tesseract: str = None):
        self.caminho_tesseract = caminho_tesseract
        pytesseract.pytesseract.tesseract_cmd = self.caminho_tesseract

    @log_de_erro
    def processar_e_classificar_unificado(self, path1, aba1, pular1, path2, aba2, pular2, cols1, cols2, dir_saida):
        return comparar_e_classificar_excel(path1, aba1, pular1, path2, aba2, pular2, cols1, cols2, dir_saida)

    @log_de_erro
    def consulta_cnpj(self, taxa_consulta=3, arquivo_entrada="cnpjs.xlsx", arquivo_saida="resultado_cnpjs.xlsx"):
        return consulta_cnpj(taxa_consulta, arquivo_entrada, arquivo_saida)

    @log_de_erro
    def dividir_excel(self, arquivo_excel=None, coluna_divisao=None, diretorio_output=None):
        return dividir_planilha_por_coluna(arquivo_excel, coluna_divisao, diretorio_output)

    @log_de_erro
    def limpar_arquivos_por_formato(self, pasta_raiz=None, formato_manter=None):
        return limpar_arquivos_por_formato(pasta_raiz, formato_manter)

    @log_de_erro
    def mover_arquivos_esocial(self, *args, **kwargs):
        return mover_arquivos_xml_metade(*args, **kwargs)

    @log_de_erro
    def organizar_xml_por_data(self, *args, **kwargs):
        return organizar_xml_por_data(*args, **kwargs)

    @log_de_erro
    def mover_arquivos_por_extensao(self, diretorio_raiz, pasta_output, extensao_desejada):
        self.tipos_restantes = mover_arquivos_por_extensao(diretorio_raiz, pasta_output, extensao_desejada)
        return self.tipos_restantes

    @log_de_erro
    def unificar_excel_da_pasta(self, pasta):
        return unificar_excel_da_pasta(pasta)

    @log_de_erro
    def dividir_pdf(self, input_pdf_path):
        return dividir_pdf(input_pdf_path)

    @log_de_erro
    def processar_pdfs_dctf(self, pasta_pdfs, usar_ocr=True):
        arquivos_pdf = listar_pdfs(pasta_pdfs)
        consolidado_df = pd.DataFrame()

        for arquivo_pdf in arquivos_pdf:
            caminho_pdf = os.path.join(pasta_pdfs, arquivo_pdf)
            print(f"[DCTF] Processando: {arquivo_pdf}")
            try:
                dctf_df, _ = extrair_dctf_pdf(caminho_pdf, usar_ocr)
                dctf_df['ARQUIVO_ORIGEM'] = arquivo_pdf
                consolidado_df = pd.concat([consolidado_df, dctf_df], ignore_index=True)
            except Exception as e:
                print(f"❌ Erro ao processar DCTF {arquivo_pdf}: {e}")
            finally:
                gc.collect()

        if not consolidado_df.empty:
            nome_saida = os.path.join(pasta_pdfs, "resultado_dctf.xlsx")
            consolidado_df.to_excel(nome_saida, index=False)
            print(f"✅ Arquivo salvo em: {nome_saida}")
        else:
            print("Nenhum dado encontrado nos PDFs.")

        gc.collect()
        return consolidado_df

    @log_de_erro
    def processar_fontes_pagadoras(self, pasta_pdfs, usar_ocr=True):
        arquivos_pdf = listar_pdfs(pasta_pdfs)
        consolidado_df = pd.DataFrame()

        if not usar_ocr:
            print("[FONTES] OCR desativado. Pulando processamento.")
            return consolidado_df

        for arquivo_pdf in arquivos_pdf:
            caminho_pdf = os.path.join(pasta_pdfs, arquivo_pdf)
            print(f"[FONTES] Processando: {arquivo_pdf}")
            try:
                imagens = pdf_to_images(caminho_pdf)
                textos = [extract_ocr_data_from_image(img, 'fonte_pagadora', config_map)[0] for img in imagens]
                texto_completo = "\n".join(textos)

                dados = find_full_patterns(texto_completo)
                if dados:
                    df = pd.DataFrame(dados, columns=['CNPJ', 'Nome', 'Data', 'Código', 'Rendimento', 'Imposto'])
                    df['ARQUIVO_ORIGEM'] = arquivo_pdf
                    consolidado_df = pd.concat([consolidado_df, df], ignore_index=True)
                else:
                    print(f"[FONTES] Nenhum dado encontrado no arquivo {arquivo_pdf}.")
            except Exception as e:
                print(f"❌ Erro ao processar Fonte Pagadora {arquivo_pdf}: {e}")
            finally:
                gc.collect()

        if not consolidado_df.empty:
            caminho_saida = os.path.join(pasta_pdfs, "Fontes_Pagadoras_Consolidado.xlsx")
            consolidado_df.to_excel(caminho_saida, index=False)
            print(f"[FONTES] Arquivo consolidado salvo em: {caminho_saida}")
        else:
            print("[FONTES] Nenhum dado encontrado para salvar.")

        gc.collect()
        return consolidado_df

    @log_de_erro
    def processar_darf_pdfs(self, pasta_pdfs, usar_ocr=True):
        if not usar_ocr:
            print("[DARF] OCR desativado. Pulando processamento.")
            return pd.DataFrame()

        arquivos_pdf = listar_pdfs(pasta_pdfs)
        consolidado_df = pd.DataFrame()

        for arquivo_pdf in arquivos_pdf:
            caminho_pdf = os.path.join(pasta_pdfs, arquivo_pdf)
            print(f"\n[DARF] Processando: {arquivo_pdf}")

            try:
                imagens = pdf_to_images(caminho_pdf, dpi=500)
                textos = []

                for idx, imagem in enumerate(tqdm(imagens, desc=f"Processando páginas de {arquivo_pdf}")):
                    try:
                        texto, conf = extract_ocr_data_from_image(imagem, 'darf', config_map)
                        textos.append(texto)
                    finally:
                        del imagem
                        gc.collect()

                records = extrair_infos_darf(caminho_pdf, arquivo_pdf)
                if records:
                    df_darf = pd.DataFrame(records)
                    df_darf['ARQUIVO_ORIGEM'] = arquivo_pdf
                    consolidado_df = pd.concat([consolidado_df, df_darf], ignore_index=True)
                    print(f"[DARF] {len(records)} registros extraídos de {arquivo_pdf}.")
                else:
                    print(f"[DARF] Nenhum registro encontrado em {arquivo_pdf}.")
            except Exception as e:
                print(f"❌ Erro ao processar DARF {arquivo_pdf}: {e}")
                continue

        if not consolidado_df.empty:
            caminho_saida = os.path.join(pasta_pdfs, "DARF_Consolidado.xlsx")
            consolidado_df.to_excel(caminho_saida, index=False)
            print(f"\n✅ [DARF] Arquivo consolidado salvo em: {caminho_saida}")
        else:
            print("\n⚠️ [DARF] Nenhum dado encontrado para salvar.")

        gc.collect()
        return consolidado_df

    # ===== Métodos de OCR livre, CFOP, DCOMP, Recolhimentos =====
    @log_de_erro
    def processar_pdfs_ocr_free(self, pasta_pdfs, usar_ocr=True):
        if not usar_ocr:
            print("[OCR_FREE] OCR desativado. Pulando processamento.")
            return pd.DataFrame()

        todas_linhas = []
        arquivos_pdf = listar_pdfs(pasta_pdfs)

        for arquivo_pdf in arquivos_pdf:
            caminho_pdf = os.path.join(pasta_pdfs, arquivo_pdf)
            imagens = pdf_to_images(caminho_pdf)
            linhas = []

            for img in imagens:
                try:
                    texto, _ = extract_ocr_data_from_image(img, 'free_tabulate', config_map)
                    linhas.extend(parse_text_free(texto))
                finally:
                    del img
                    gc.collect()

            todas_linhas.extend(linhas)
            gc.collect()

        if not todas_linhas:
            return pd.DataFrame()

        colunas = ['Data', 'Numero', 'Descricao', 'Quantidade', 'Valor', 'Debito/Credito', 'Conta', 'Saldo Anterior']
        df = pd.DataFrame(todas_linhas, columns=colunas)
        caminho_saida = os.path.join(pasta_pdfs, "OCR_Free_Consolidado.xlsx")
        df.to_excel(caminho_saida, index=False)
        gc.collect()
        return df

    @log_de_erro
    def processar_cfop_pdfs(self, pasta_pdfs, usar_ocr=True):
        if not usar_ocr:
            print("[CFOP] OCR desativado. Pulando processamento.")
            return pd.DataFrame()

        todos = []
        for pdf_path in Path(pasta_pdfs).glob("*.pdf"):
            nome_arquivo = pdf_path.name
            imagens = pdf_to_images(pdf_path)
            for i, img in enumerate(imagens, start=1):
                print(f"📄 Processando {nome_arquivo} - página {i}")
                img = img.convert('RGB')
                img_proc = preprocess_cfop_image(img)
                texto, _ = extract_ocr_data_from_image(img_proc, 'cfop', config_map)
                registros = extrair_cfop_valores(texto, nome_arquivo, i)
                todos.extend(registros)

                del img, img_proc, texto, registros
                gc.collect()
            del imagens
            gc.collect()

        if not todos:
            print("[CFOP] Nenhum dado encontrado para salvar.")
            return pd.DataFrame()

        df = pd.DataFrame(todos)
        caminho_saida = os.path.join(pasta_pdfs, "CFOP_Consolidado.xlsx")
        df.to_excel(caminho_saida, index=False)
        print(f"[CFOP] Arquivo consolidado salvo em: {caminho_saida}")
        return df

    @log_de_erro
    def processar_dcomp_pdfs(self, pasta_pdfs, usar_ocr=True):
        try:
            df = processar_dcomp(pasta_pdfs, usar_ocr)
            gc.collect()
            return df
        except Exception as e:
            print(f"❌ Erro ao processar DCOMP: {e}")
            gc.collect()
            return pd.DataFrame()

    @log_de_erro
    def processar_dcomp_ipi_pdfs(self, pasta_pdfs, usar_ocr=False):
        try:
            df = processor_dcomp_ipi(pasta_pdfs, usar_ocr)
            gc.collect()
            return df
        except Exception as e:
            print(f"❌ Erro ao processar DCOMP IPI: {e}")
            gc.collect()
            return pd.DataFrame()

    @log_de_erro
    def processar_recolhimentos_pdfs(self, pasta_pdfs, usar_ocr=False):
        print(f"[RECOLHIMENTOS] Processando PDFs em: {pasta_pdfs} com OCR={usar_ocr}")
        try:
            df_recolhimentos = extrair_recolhimento_pdf(pasta_pdfs, usar_ocr=usar_ocr)
            if not df_recolhimentos.empty:
                print(f"[RECOLHIMENTOS] Extração concluída. {len(df_recolhimentos)} registros encontrados.")
            else:
                print("[RECOLHIMENTOS] Nenhum dado encontrado.")
            gc.collect()
            return df_recolhimentos
        except Exception as e:
            print(f"❌ Erro ao processar Recolhimentos: {e}")
            gc.collect()
            return pd.DataFrame()

    # ===== Wrappers para RegistroIPI =====
    @log_de_erro
    def processar_r11_r12(self, arquivo_excel, diretorio_saida):
        gerador = RegistroIPI()
        return gerador.processar_r11_r12(arquivo_excel, diretorio_saida)

    @log_de_erro
    def processar_r13(self, arquivo_excel, diretorio_saida):
        gerador = RegistroIPI()
        return gerador.processar_r13(arquivo_excel, diretorio_saida)

    @log_de_erro
    def processar_r15(self, arquivo_excel, diretorio_saida):
        gerador = RegistroIPI()
        return gerador.processar_r15(arquivo_excel, diretorio_saida)

    @log_de_erro
    def processar_r21(self, arquivo_excel, diretorio_saida):
        gerador = RegistroIPI()
        return gerador.processar_r21(arquivo_excel, diretorio_saida)
