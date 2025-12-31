import os
import logging
import pandas as pd


def dividir_planilha_por_coluna(arquivo_excel, coluna_para_divisao, diretorio_output=None):

    if not os.path.isfile(arquivo_excel):
        logging.error(f"Arquivo Excel inválido ou inexistente: {arquivo_excel}")
        return

    if diretorio_output is None:
        diretorio_output = os.path.join(os.getcwd(), "output")
    if not os.path.exists(diretorio_output):
        os.makedirs(diretorio_output)
        logging.info(f"Pasta criada: {diretorio_output}")

    try:
        df = pd.read_excel(arquivo_excel)
        logging.info(f"Arquivo carregado: {arquivo_excel}")

        if coluna_para_divisao not in df.columns:
            logging.error(f"Coluna '{coluna_para_divisao}' não encontrada na planilha.")
            return

        # Se a coluna for datetime, cria coluna 'MesAno' para divisão
        if pd.api.types.is_datetime64_any_dtype(df[coluna_para_divisao]):
            df[coluna_para_divisao] = pd.to_datetime(df[coluna_para_divisao])
            df["MesAno"] = df[coluna_para_divisao].dt.strftime("%Y-%m")
            coluna_para_dividir = "MesAno"
            logging.info(
                f"Coluna '{coluna_para_divisao}' é data, criando coluna 'MesAno' para divisão."
            )
        else:
            coluna_para_dividir = coluna_para_divisao

        valores_unicos = df[coluna_para_dividir].unique()
        logging.info(
            f"Valores únicos para divisão na coluna '{coluna_para_dividir}': {len(valores_unicos)}"
        )

        for valor in valores_unicos:
            df_filtrado = df[df[coluna_para_dividir] == valor]
            nome_arquivo_saida = f"{valor}.xlsx"
            caminho_saida = os.path.join(diretorio_output, nome_arquivo_saida)
            df_filtrado.to_excel(caminho_saida, index=False)
            logging.info(f"Arquivo salvo: {caminho_saida}")

        logging.info("Processamento da planilha concluído com sucesso.")

    except Exception as e:
        logging.error(f"Erro durante o processamento da planilha: {e}")
