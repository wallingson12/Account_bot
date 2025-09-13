from services.comparador import comparar_e_classificar_excel
from services.consult_cnpj import consulta_cnpj
from services.dividir_excel import dividir_planilha_por_coluna
from services.limpar_pasta import limpar_arquivos_por_formato
from services.mover_arquivos_esocial import (
    mover_arquivos_xml_metade,
    organizar_xml_por_data,
)
from services.mover_arquivos_por_extensao import mover_arquivos_por_extensao
from services.unificar_excel import (
    unificar_excel_da_pasta
)

from services.divisor_pdf import dividir_pdf
from account_tools.utils.decorators import log_de_erro

import os
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

from dcomp_file.R11_R12_DCOMP import *

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
        """Realiza conciliação de planilhas Excel, com classificação automática.

        Parâmetros:
            **kwargs: Argumentos a serem repassados para a função interna `comparar_e_classificar_excel`.

        Retorna:
            Resultado da conciliação e classificação, geralmente um DataFrame com os dados organizados.
        """
        return comparar_e_classificar_excel(path1, aba1, pular1, path2, aba2, pular2, cols1, cols2, dir_saida)

    @log_de_erro
    def consulta_cnpj(self, taxa_consulta=3, arquivo_entrada="cnpjs.xlsx", arquivo_saida="resultado_cnpjs.xlsx"):
        """Realiza a consulta de informações para cada CNPJ presente na coluna 'CNPJ'.

        Parâmetros:
            **kwargs: Argumentos a serem repassados para a função interna `consulta_cnpj`.

        Retorna:
            Resultado da consulta, geralmente um DataFrame ou dicionário com os dados dos CNPJs.
        """
        return consulta_cnpj(taxa_consulta=3, arquivo_entrada="cnpjs.xlsx", arquivo_saida="resultado_cnpjs.xlsx")

    @log_de_erro
    def dividir_excel(
            self, arquivo_excel=None, coluna_divisao=None, diretorio_output=None
    ):

        """Divide uma planilha Excel em múltimos arquivos, com base nos valores de uma coluna.

        Parâmetros:
            arquivo_excel (str): Caminho para o arquivo Excel que será dividido.
            coluna_divisao (str): Nome da coluna que será usada como critério de divisão.
            diretorio_output (str): Diretório onde os arquivos divididos serão salvos.

        Retorna:
            None. Os arquivos resultantes são salvos diretamente no diretório especificado.
        """
        return dividir_planilha_por_coluna(
            arquivo_excel=arquivo_excel,
            coluna_divisao=coluna_divisao,
            diretorio_output=diretorio_output, )

    @log_de_erro
    def limpar_arquivos_por_formato(self, pasta_raiz=None, formato_manter=None):

        """Remove arquivos de uma pasta, mantendo apenas os com o formato especificado.

        Parâmetros:
            pasta_raiz (str): Caminho para a pasta onde os arquivos serão verificados.
            formato_manter (str): Extensão dos arquivos que devem ser mantidos (ex: '.xml').

        Retorna:
            None. Os arquivos não correspondentes ao formato são removidos diretamente da pasta.
        """
        return limpar_arquivos_por_formato(
            pasta_raiz=pasta_raiz, formato_manter=formato_manter)

    @log_de_erro
    def mover_arquivos_esocial(self, *args, **kwargs):
        """Move arquivos XML da pasta base para a pasta destino, com opção de mover apenas metade.

        Parâmetros:
        pasta_base (str): Caminho da pasta onde os arquivos XML estão localizados.
        pasta_destino (str): Caminho da pasta para onde os arquivos serão movidos.
        dividir (bool): Se True, move apenas metade dos arquivos XML da pasta base (não recursivo).
                        Se False, move todos os arquivos XML recursivamente.

        Retorna:
        None. Os arquivos são movidos diretamente para a pasta destino.
        """
        return mover_arquivos_xml_metade(*args, **kwargs)

    @log_de_erro
    def organizar_xml_por_data(self, *args, **kwargs):
        """Organiza arquivos XML em subpastas com base na data de emissão (dhEmi).

        A função analisa cada arquivo XML no diretório especificado e extrai a data de emissão
        (usando a tag 'dhEmi', 'dEmi', 'perApur' ou similar). Com base nessa data, os arquivos
        são movidos para subpastas organizadas por ano ou por mês/ano.

        Parâmetros:
            diretorio (str): Caminho da pasta contendo os arquivos XML a serem organizados.
            organizar_por (str): Critério de organização. Pode ser:
                - "ano": cria pastas com o ano da emissão (ex: '2024').
                - "mes/ano": cria pastas com mês e ano (ex: '06-2024').

        Retorna:
            None. Os arquivos XML são movidos para as subpastas criadas dentro do diretório informado.
        """
        return organizar_xml_por_data(*args, **kwargs)

    @log_de_erro
    def mover_arquivos_por_extensao(
            self, diretorio_raiz, pasta_output, extensao_desejada
    ):

        """Move arquivos com uma determinada extensão de uma pasta (e seus subdiretórios) para uma pasta de saída.

        A função percorre recursivamente o diretório raiz e move todos os arquivos que possuem
        a extensão desejada para a pasta de destino. Caso existam nomes repetidos, arquivos são
        renomeados para evitar sobrescrita. Arquivos com outras extensões são contabilizados.

        Parâmetros:
            diretorio_raiz (str): Caminho da pasta onde a busca pelos arquivos será iniciada.
            pasta_output (str): Caminho da pasta de destino onde os arquivos serão movidos.
            extensao_desejada (str): Extensão dos arquivos a serem movidos (ex: '.xml', 'pdf').

        Retorna:
            dict: Um dicionário com as extensões restantes e a quantidade de arquivos não movidos,
                organizado por extensão.
        """
        # Atualiza o dicionário interno com o resultado da função
        self.tipos_restantes = mover_arquivos_por_extensao(
            diretorio_raiz, pasta_output, extensao_desejada)
        return self.tipos_restantes

    @log_de_erro
    def unificar_excel_da_pasta(self, pasta):
        """Lê e unifica todos os arquivos Excel (.xls, .xlsx) de uma pasta em um único arquivo.

        A função carrega paralelamente todos os arquivos Excel da pasta especificada,
        concatena os dados em um único DataFrame e salva o resultado como 'unificados.xlsx'
        dentro da mesma pasta. Gera logs informativos sobre o processo.

        Parâmetros:
            pasta (str): Caminho da pasta contendo os arquivos Excel a serem unificados.

        Retorna:
            str | None: Caminho do arquivo Excel unificado gerado, ou None em caso de erro ou se não houver arquivos válidos.
        """
        return unificar_excel_da_pasta(pasta)

    @log_de_erro
    def dividir_pdf(self, input_pdf_path):
        """
        Parâmetros: input_pdf_path(str)

        Retorna: Divide o PDF em páginas.
        """
        return dividir_pdf(input_pdf_path)

    @log_de_erro
    def processar_pdfs_dctf(self, pasta_pdfs, usar_ocr=True):
        """
        Processa arquivos PDF de DCTF em uma pasta, aplicando OCR (se habilitado) e
        consolidando os registros extraídos em um único DataFrame e planilha Excel.

        Args:
            pasta_pdfs (str | Path): Caminho da pasta contendo os arquivos PDF de DCTF.
            usar_ocr (bool, optional): Define se OCR deve ser utilizado.
                Padrão=True.

        Returns:
            pandas.DataFrame: DataFrame consolidado com os registros extraídos.
                Retorna vazio se não houver dados.

        Side Effects:
            - Cria o arquivo `resultado_dctf.xlsx` na mesma pasta.
            - Imprime logs de progresso no console.
        """
        arquivos_pdf = listar_pdfs(pasta_pdfs)
        consolidado_df = pd.DataFrame()

        for arquivo_pdf in arquivos_pdf:
            caminho_pdf = os.path.join(pasta_pdfs, arquivo_pdf)
            print(f"[DCTF] Processando: {arquivo_pdf}")
            try:
                dctf_df, _ = extrair_dctf_pdf(caminho_pdf=caminho_pdf, usar_ocr=usar_ocr)
                dctf_df['ARQUIVO_ORIGEM'] = arquivo_pdf
                consolidado_df = pd.concat([consolidado_df, dctf_df], ignore_index=True)
            except Exception as e:
                print(f"❌ Erro ao processar DCTF {arquivo_pdf}: {e}")
            finally:
                gc.collect()  # libera memória após processar cada PDF

        if not consolidado_df.empty:
            nome_saida = os.path.join(pasta_pdfs, "resultado_dctf.xlsx")
            consolidado_df.to_excel(nome_saida, index=False)
            print(f"✅ Arquivo salvo em: {nome_saida}")
            gc.collect()  # garante limpeza final de memória
            return consolidado_df
        else:
            print("Nenhum dado encontrado nos PDFs.")
            gc.collect()  # limpeza caso não haja dados
            return pd.DataFrame()

    @log_de_erro
    def processar_fontes_pagadoras(self, pasta_pdfs, usar_ocr=True):
        """
            Processa todos os arquivos PDF de Fontes Pagadoras em uma pasta, aplicando OCR
            e extraindo os dados estruturados (CNPJ, Nome, Data, Código, Rendimento, Imposto).
            O resultado é consolidado em um único DataFrame e salvo em Excel.

            Fluxo:
                1. Lista todos os PDFs da pasta informada.
                2. Converte cada PDF em imagens de página.
                3. Aplica OCR em cada imagem para extrair o texto bruto.
                4. Executa o parser (`find_full_patterns`) para localizar os padrões desejados.
                5. Monta DataFrames individuais por arquivo e adiciona a coluna 'ARQUIVO_ORIGEM'.
                6. Concatena todos os DataFrames em um consolidado único.
                7. Salva o resultado em "Fontes_Pagadoras_Consolidado.xlsx".

            Args:
                pasta_pdfs (str): Caminho da pasta contendo os arquivos PDF.
                usar_ocr (bool, opcional): Define se OCR deve ser utilizado.
                    Padrão é True.

            Returns:
                pandas.DataFrame: Consolidado com os dados extraídos.
                                  Se nenhum dado for encontrado, retorna DataFrame vazio.

            Raises:
                Exception: Erros individuais por arquivo são tratados internamente.
                           Se todos falharem, retorna DataFrame vazio sem lançar exceção.
        """
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
                gc.collect()  # libera memória após processar cada PDF

        if not consolidado_df.empty:
            caminho_saida = os.path.join(pasta_pdfs, "Fontes_Pagadoras_Consolidado.xlsx")
            consolidado_df.to_excel(caminho_saida, index=False)
            print(f"[FONTES] Arquivo consolidado salvo em: {caminho_saida}")
            gc.collect()  # limpeza final após salvar o arquivo
        else:
            print("[FONTES] Nenhum dado encontrado para salvar.")
            gc.collect()  # limpeza caso não haja dados

        return consolidado_df

    @log_de_erro
    def processar_darf_pdfs(self, pasta_pdfs, usar_ocr=True):
        """
        Processa arquivos PDF de DARF, aplicando OCR (se habilitado) e consolidando
        os registros extraídos em um DataFrame e planilha Excel.

        Args:
            pasta_pdfs (str | Path): Caminho da pasta contendo os PDFs de DARF.
            usar_ocr (bool, optional): Define se OCR deve ser utilizado.
                Padrão=True.

        Returns:
            pandas.DataFrame: Dados extraídos dos PDFs de DARF. Retorna vazio
                se não houver registros.

        Side Effects:
            - Cria o arquivo `DARF_Consolidado.xlsx`.
            - Exibe logs detalhados de cada página processada.
        """
        if not usar_ocr:
            print("[DARF] OCR desativado. Pulando processamento.")
            return pd.DataFrame()

        arquivos_pdf = listar_pdfs(pasta_pdfs)
        consolidado_df = pd.DataFrame()

        for arquivo_pdf in arquivos_pdf:
            caminho_pdf = os.path.join(pasta_pdfs, arquivo_pdf)
            print(f"\n[DARF] Processando: {arquivo_pdf}")

            try:
                imagens = pdf_to_images(caminho_pdf, dpi=500)  # Reduzido para evitar consumo de memória
                textos = []

                for idx, imagem in enumerate(tqdm(imagens, desc=f"Processando páginas de {arquivo_pdf}")):
                    try:
                        texto, conf = extract_ocr_data_from_image(imagem, 'darf', config_map)
                        textos.append(texto)
                    except Exception as e_img:
                        print(f"[DARF] Erro na página {idx + 1} de {arquivo_pdf}: {e_img}")
                    finally:
                        del imagem
                        gc.collect()

                texto_completo = "\n".join(textos)

                # Extração estruturada de dados após OCR
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

        return consolidado_df

    @log_de_erro
    def processar_pdfs_ocr_free(self, pasta_pdfs, usar_ocr=True):
        """
        Processa PDFs genéricos em formato tabular (OCR livre), aplicando OCR
        e consolidando os dados em um DataFrame.

        Args:
            pasta_pdfs (str | Path): Caminho da pasta com os PDFs.
            usar_ocr (bool, optional): Se True, aplica OCR. Padrão=True.

        Returns:
            pandas.DataFrame: DataFrame com os dados tabulares extraídos.
                Retorna vazio se nenhum dado for identificado.

        Side Effects:
            - Cria o arquivo `OCR_Free_Consolidado.xlsx`.
        """
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
                    gc.collect()  # libera memória após cada imagem

            todas_linhas.extend(linhas)
            gc.collect()  # limpa memória após cada PDF

        if not todas_linhas:
            gc.collect()
            return pd.DataFrame()

        colunas = ['Data', 'Numero', 'Descricao', 'Quantidade', 'Valor', 'Debito/Credito', 'Conta', 'Saldo Anterior']
        df = pd.DataFrame(todas_linhas, columns=colunas)
        caminho_saida = os.path.join(pasta_pdfs, "OCR_Free_Consolidado.xlsx")
        df.to_excel(caminho_saida, index=False)
        gc.collect()  # limpeza final após salvar o arquivo

        return df

    @log_de_erro
    def processar_cfop_pdfs(self, pasta_pdfs, usar_ocr=True):
        """
                Processa todos os arquivos PDF de CFOP em uma pasta, aplicando OCR e extraindo
                os registros estruturados para consolidação em planilha Excel.

                Fluxo:
                    1. Lista todos os PDFs no diretório informado.
                    2. Converte cada página em imagem e aplica pré-processamento otimizado para CFOP.
                    3. Executa OCR em cada página processada.
                    4. Extrai os registros de CFOP via `extrair_cfop_valores`.
                    5. Consolida os dados em um DataFrame único e salva como "CFOP_Consolidado.xlsx".

                Args:
                    pasta_pdfs (str): Caminho da pasta contendo os PDFs de CFOP.
                    usar_ocr (bool, opcional): Indica se o OCR deve ser executado.
                        - True (padrão): processa normalmente.
                        - False: retorna DataFrame vazio sem processar.

                Returns:
                    pandas.DataFrame: DataFrame com os registros extraídos.
                                      Caso nenhum dado seja encontrado, retorna vazio.
                """
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

                # Limpeza de memória da imagem processada
                del img, img_proc, texto, registros
                gc.collect()

            # Limpeza de memória após cada PDF
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
        """
                Processa os arquivos PDF de DCOMP em uma pasta, aplicando OCR quando necessário
                e consolidando os resultados em um DataFrame.

                Args:
                    pasta_pdfs (str): Caminho da pasta contendo os PDFs de DCOMP.
                    usar_ocr (bool, opcional): Define se OCR deve ser utilizado (padrão=True).

                Returns:
                    pandas.DataFrame: Dados extraídos dos PDFs de DCOMP.
                                      Retorna vazio em caso de falha ou ausência de registros.

                Observação:
                    A extração é realizada pela função `processar_dcomp`.
                """
        try:
            df = processar_dcomp(pasta_pdfs, usar_ocr)
            gc.collect()  # coleta de memória após processamento
            return df
        except Exception as e:
            print(f"❌ Erro ao processar DCOMP: {e}")
            gc.collect()
            return pd.DataFrame()

    @log_de_erro
    def processar_dcomp_ipi_pdfs(self, pasta_pdfs, usar_ocr=False):
        """
                Processa arquivos PDF de DCOMP IPI em uma pasta, aplicando OCR quando solicitado
                e retornando os dados extraídos em formato estruturado.

                Args:
                    pasta_pdfs (str): Caminho da pasta com os PDFs de DCOMP IPI.
                    usar_ocr (bool, opcional): Indica se OCR deve ser utilizado.
                        Padrão=False.

                Returns:
                    pandas.DataFrame: DataFrame com os registros extraídos.
                                      Caso não haja dados ou ocorra erro, retorna vazio.

                Observação:
                    A extração é delegada à função `processor_dcomp_ipi`.
                """
        try:
            df = processor_dcomp_ipi(pasta_pdfs, usar_ocr)
            gc.collect()  # coleta de memória após processamento
            return df
        except Exception as e:
            print(f"❌ Erro ao processar DCOMP IPI: {e}")
            gc.collect()
            return pd.DataFrame()

    @log_de_erro
    def processar_recolhimentos_pdfs(self, pasta_pdfs, usar_ocr=False):
        """
                Processa arquivos PDF de Recolhimentos, aplicando OCR quando necessário
                e consolidando os registros em DataFrame.

                Args:
                    pasta_pdfs (str): Caminho da pasta com os PDFs de Recolhimentos.
                    usar_ocr (bool, opcional): Define se OCR deve ser usado. Padrão=False.

                Returns:
                    pandas.DataFrame: Dados extraídos dos PDFs.
                                      Retorna vazio se nenhum registro for encontrado ou se ocorrer erro.

                Observação:
                    A extração é feita pela função `extrair_recolhimento_pdf`.
                """
        print(f"[RECOLHIMENTOS] Processando PDFs em: {pasta_pdfs} com OCR={usar_ocr}")
        try:
            df_recolhimentos = extrair_recolhimento_pdf(pasta_pdfs, usar_ocr=usar_ocr)
            if not df_recolhimentos.empty:
                print(f"[RECOLHIMENTOS] Extração concluída. {len(df_recolhimentos)} registros encontrados.")
            else:
                print("[RECOLHIMENTOS] Nenhum dado encontrado.")
            gc.collect()  # coleta de memória após processamento
            return df_recolhimentos
        except Exception as e:
            print(f"❌ Erro ao processar Recolhimentos: {e}")
            gc.collect()
            return pd.DataFrame()

    @log_de_erro
    def process_file_r11_r12(self, file_path):
        """
        Processa arquivos Excel do tipo R11/R12 (DCOMP), validando colunas e
        gerando arquivo de saída `.txt`.

        Args:
            file_path (str | Path): Caminho do arquivo Excel a ser processado.

        Returns:
            str: Caminho do arquivo `.txt` gerado.

        Side Effects:
            - Cria arquivo `.txt` com o mesmo nome do Excel de entrada.
        """
        df = carregar_excel(file_path)
        df = validar_colunas_valores(df)
        df, _ = formatar_dados(df)

        df['Operações com Crédito do Imposto - Base de Cálculo'] = df[
            'Operações com Crédito do Imposto - Base de Cálculo'].apply(lambda x: f'{x:,.2f}'.replace('.', ','))
        df['Operações com Crédito do Imposto - IPI Creditado'] = df[
            'Operações com Crédito do Imposto - IPI Creditado'].apply(lambda x: f'{x:,.2f}'.replace('.', ','))
        df['Operações sem Crédito do Imposto - Isentas ou Não Tributadas'] = df[
            'Operações sem Crédito do Imposto - Isentas ou Não Tributadas'].apply(
            lambda x: f'{x:,.2f}'.replace('.', ','))
        df['Operações sem Crédito do Imposto - Outras'] = df[
            'Operações sem Crédito do Imposto - Outras'].apply(lambda x: f'{x:,.2f}'.replace('.', ','))

        lines = df.apply(generate_line, axis=1)

        file_type = df['Tipo'].iloc[0]
        output_path = rf"{file_type}.txt"

        with open(output_path, "w") as file:
            file.writelines(lines)

        return output_path