import logging
import os
import pandas as pd

green = "\033[92m"
reset = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(message)s")


def print_verde(msg):
    print(f"{green}{msg}{reset}")


def limpar_entrada(texto):
    return texto.strip().strip('"').strip("'")


def classificar_conciliacao_excel(
    caminho_excel_origem: str,
    aba_origem: str,
    linhas_pular_origem: int,
    caminho_excel_destino: str,
    aba_destino: str,
    linhas_pular_destino: int,
    colunas_chave_origem: list,
    colunas_chave_destino: list,
    diretorio_saida: str,
):
    """
    Processa e classifica dois arquivos Excel comparando chaves compostas.
    Salva os arquivos classificados em dir_saida.
    """
    # Limpa entradas
    caminho_excel_origem = limpar_entrada(caminho_excel_origem)
    aba_origem = limpar_entrada(aba_origem)
    caminho_excel_destino = limpar_entrada(caminho_excel_destino)
    aba_destino = limpar_entrada(aba_destino)
    dir_saida = limpar_entrada(diretorio_saida)

    if not os.path.isdir(dir_saida):
        logging.error(f"[ERRO] Diretório inválido: {dir_saida}")
        return

    nome_arquivo_origem = os.path.splitext(os.path.basename(caminho_excel_origem))[0]
    nome_arquivo_destino = os.path.splitext(os.path.basename(caminho_excel_destino))[0]

    caminho_saida_origem = os.path.join(dir_saida, f"{nome_arquivo_origem}_Classificado.xlsx")
    caminho_saida_destino = os.path.join(dir_saida, f"{nome_arquivo_destino}_Classificado.xlsx")

    try:
        df_origem = pd.read_excel(caminho_excel_origem, sheet_name=aba_origem, skiprows=linhas_pular_origem, engine="openpyxl")
        print_verde(f"[INFO] Planilha carregada: {caminho_excel_origem} - Aba: {aba_origem}")
        print_verde(f"[INFO] Colunas: {df_origem.columns.tolist()}")
    except Exception as e:
        logging.error(f"[ERRO] Falha ao carregar {caminho_excel_origem}:\n{e}")
        return

    try:
        df_destino = pd.read_excel(caminho_excel_destino, sheet_name=aba_destino, skiprows=linhas_pular_destino, engine="openpyxl")
        print_verde(f"[INFO] Planilha carregada: {caminho_excel_destino} - Aba: {aba_destino}")
        print_verde(f"[INFO] Colunas: {df_destino.columns.tolist()}")
    except Exception as e:
        logging.error(f"[ERRO] Falha ao carregar {caminho_excel_destino}:\n{e}")
        return

    faltantes1 = [c for c in colunas_chave_origem if c not in df_origem.columns]
    if faltantes1:
        logging.error(
            f"[ERRO] Colunas não encontradas no primeiro arquivo: {faltantes1}"
        )
        return
    df_origem = df_origem.copy()
    df_origem["chave"] = (
        df_origem[colunas_chave_origem]
        .astype(str)
        .apply(lambda row: "_".join([val.strip() for val in row.values]), axis=1)
    )
    print_verde(
        f"[INFO] Coluna chave 'chave' criada no primeiro arquivo a partir de {colunas_chave_origem}"
    )

    faltantes2 = [c for c in colunas_chave_destino if c not in df_destino.columns]
    if faltantes2:
        logging.error(
            f"[ERRO] Colunas não encontradas no segundo arquivo: {faltantes2}"
        )
        return
    df_destino = df_destino.copy()
    df_destino["chave"] = (
        df_destino[colunas_chave_destino]
        .astype(str)
        .apply(lambda row: "_".join([val.strip() for val in row.values]), axis=1)
    )
    print_verde(
        f"[INFO] Coluna chave 'chave' criada no segundo arquivo a partir de {colunas_chave_destino}"
    )

    chaves1 = set(df_origem["chave"])
    chaves2 = set(df_destino["chave"])

    try:
        contagem = df_origem["chave"].value_counts()

        def classificar_linha_origem(chave):
            if contagem.get(chave, 0) > 1:
                return "Excluir"
            elif chave in chaves2:
                return "Correto"
            else:
                return "Estudar"

        df_origem_classificado = df_origem.copy()
        df_origem_classificado["Classificação"] = df_origem_classificado["chave"].apply(classificar_linha_origem)
        print_verde(f"[INFO] Classificação do primeiro arquivo concluída")
    except Exception as e:
        logging.error(f"[ERRO] Erro classificando primeiro arquivo:\n{e}")
        df_origem_classificado = df_origem.copy()

    try:
        df_destino_classificado = df_destino.copy()
        df_destino_classificado["Classificação"] = df_destino_classificado["chave"].apply(
            lambda chave: "Correto" if chave in chaves1 else "Incluir"
        )
        print_verde(f"[INFO] Classificação complementar do segundo arquivo concluída")
    except Exception as e:
        logging.error(f"[ERRO] Erro classificando segundo arquivo:\n{e}")
        df_destino_classificado = df_destino.copy()

    try:
        if os.path.exists(caminho_saida_origem):
            with pd.ExcelWriter(
                caminho_saida_origem, engine="openpyxl", mode="a", if_sheet_exists="replace"
            ) as writer:
                df_origem_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(f"[INFO] Aba 'Classificado' salva em: {caminho_saida_origem}")
        else:
            with pd.ExcelWriter(caminho_saida_origem, engine="openpyxl", mode="w") as writer:
                df_origem_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(
                f"[INFO] Novo arquivo criado e aba 'Classificado' salva: {caminho_saida_origem}"
            )
    except Exception as e:
        logging.error(f"[ERRO] Erro ao salvar arquivo {caminho_saida_origem}:\n{e}")

    try:
        if os.path.exists(caminho_saida_destino):
            with pd.ExcelWriter(
                caminho_saida_destino, engine="openpyxl", mode="a", if_sheet_exists="replace"
            ) as writer:
                df_destino_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(f"[INFO] Aba 'Classificado' salva em: {caminho_saida_destino}")
        else:
            with pd.ExcelWriter(caminho_saida_destino, engine="openpyxl", mode="w") as writer:
                df_destino_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(
                f"[INFO] Novo arquivo criado e aba 'Classificado' salva: {caminho_saida_destino}"
            )
    except Exception as e:
        logging.error(f"[ERRO] Erro ao salvar arquivo {caminho_saida_destino}:\n{e}")
