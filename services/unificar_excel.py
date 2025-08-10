import os
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def unificar_excel_da_pasta(pasta):
    """
    Lê todos os arquivos Excel (.xls, .xlsx) de uma pasta, unifica-os e salva como 'unificados.xlsx'.

    :param pasta: caminho da pasta onde estão os arquivos Excel
    """
    if not os.path.isdir(pasta):
        logging.error(f"Pasta inválida ou inexistente: {pasta}")
        return None

    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith((".xlsx", ".xls"))]
    if not arquivos:
        logging.warning("Nenhum arquivo Excel encontrado na pasta.")
        return None

    total_linhas_previsto = 0

    def carregar_excel(arquivo):
        nonlocal total_linhas_previsto
        caminho = os.path.join(pasta, arquivo)
        try:
            df = pd.read_excel(caminho, engine="openpyxl")
            total_linhas_previsto += df.shape[0]
            logging.info(f"Arquivo {arquivo} lido com sucesso! {df.shape[0]} linhas.")
            return df if not df.empty else None
        except Exception as e:
            logging.error(f"Erro ao ler {arquivo}: {e}")
            return None

    logging.info("Iniciando leitura dos arquivos...")
    with ThreadPoolExecutor() as executor:
        dfs = [df for df in executor.map(carregar_excel, arquivos) if df is not None]

    logging.info(f"Total de linhas previsto: {total_linhas_previsto}")

    if not dfs:
        logging.warning("Nenhum dado válido para unificação.")
        return None

    logging.info("Iniciando concatenação...")
    try:
        df_final = pd.concat(dfs, ignore_index=True)
        total_linhas_real = df_final.shape[0]
        logging.info(f"Total de linhas após unificação: {total_linhas_real}")

        if total_linhas_real == total_linhas_previsto:
            logging.info("Unificação bem-sucedida, aguarde a geração do arquivo!")
        else:
            logging.warning("Aviso: contagem final de linhas difere do previsto!")

        destino = os.path.join(pasta, "unificados.xlsx")
        df_final.to_excel(destino, index=False, engine="openpyxl")
        logging.info(f"Arquivo salvo em: {destino}")

        return destino  # opcional, retorna o caminho do arquivo salvo

    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo: {e}")
        return None
