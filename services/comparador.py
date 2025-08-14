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


def comparar_e_classificar_excel(
    path1: str,
    aba1: str,
    pular1: int,
    path2: str,
    aba2: str,
    pular2: int,
    cols1: list,
    cols2: list,
    dir_saida: str,
):
    """
    Processa e classifica dois arquivos Excel comparando chaves compostas.
    Salva os arquivos classificados em dir_saida.
    """
    # Limpa entradas
    path1 = limpar_entrada(path1)
    aba1 = limpar_entrada(aba1)
    path2 = limpar_entrada(path2)
    aba2 = limpar_entrada(aba2)
    dir_saida = limpar_entrada(dir_saida)

    if not os.path.isdir(dir_saida):
        logging.error(f"[ERRO] Diretório inválido: {dir_saida}")
        return

    nome1 = os.path.splitext(os.path.basename(path1))[0]
    nome2 = os.path.splitext(os.path.basename(path2))[0]

    out1 = os.path.join(dir_saida, f"{nome1}_Classificado.xlsx")
    out2 = os.path.join(dir_saida, f"{nome2}_Classificado.xlsx")

    try:
        df1 = pd.read_excel(path1, sheet_name=aba1, skiprows=pular1, engine="openpyxl")
        print_verde(f"[INFO] Planilha carregada: {path1} - Aba: {aba1}")
        print_verde(f"[INFO] Colunas: {df1.columns.tolist()}")
    except Exception as e:
        logging.error(f"[ERRO] Falha ao carregar {path1}:\n{e}")
        return

    try:
        df2 = pd.read_excel(path2, sheet_name=aba2, skiprows=pular2, engine="openpyxl")
        print_verde(f"[INFO] Planilha carregada: {path2} - Aba: {aba2}")
        print_verde(f"[INFO] Colunas: {df2.columns.tolist()}")
    except Exception as e:
        logging.error(f"[ERRO] Falha ao carregar {path2}:\n{e}")
        return

    faltantes1 = [c for c in cols1 if c not in df1.columns]
    if faltantes1:
        logging.error(
            f"[ERRO] Colunas não encontradas no primeiro arquivo: {faltantes1}"
        )
        return
    df1 = df1.copy()
    df1["chave"] = (
        df1[cols1]
        .astype(str)
        .apply(lambda row: "_".join([val.strip() for val in row.values]), axis=1)
    )
    print_verde(
        f"[INFO] Coluna chave 'chave' criada no primeiro arquivo a partir de {cols1}"
    )

    faltantes2 = [c for c in cols2 if c not in df2.columns]
    if faltantes2:
        logging.error(
            f"[ERRO] Colunas não encontradas no segundo arquivo: {faltantes2}"
        )
        return
    df2 = df2.copy()
    df2["chave"] = (
        df2[cols2]
        .astype(str)
        .apply(lambda row: "_".join([val.strip() for val in row.values]), axis=1)
    )
    print_verde(
        f"[INFO] Coluna chave 'chave' criada no segundo arquivo a partir de {cols2}"
    )

    chaves1 = set(df1["chave"])
    chaves2 = set(df2["chave"])

    try:
        contagem = df1["chave"].value_counts()

        def regra(chave):
            if contagem.get(chave, 0) > 1:
                return "Excluir"
            elif chave in chaves2:
                return "Correto"
            else:
                return "Estudar"

        df1_classificado = df1.copy()
        df1_classificado["Classificação"] = df1_classificado["chave"].apply(regra)
        print_verde(f"[INFO] Classificação do primeiro arquivo concluída")
    except Exception as e:
        logging.error(f"[ERRO] Erro classificando primeiro arquivo:\n{e}")
        df1_classificado = df1.copy()

    try:
        df2_classificado = df2.copy()
        df2_classificado["Classificação"] = df2_classificado["chave"].apply(
            lambda chave: "Correto" if chave in chaves1 else "Incluir"
        )
        print_verde(f"[INFO] Classificação complementar do segundo arquivo concluída")
    except Exception as e:
        logging.error(f"[ERRO] Erro classificando segundo arquivo:\n{e}")
        df2_classificado = df2.copy()

    try:
        if os.path.exists(out1):
            with pd.ExcelWriter(
                out1, engine="openpyxl", mode="a", if_sheet_exists="replace"
            ) as writer:
                df1_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(f"[INFO] Aba 'Classificado' salva em: {out1}")
        else:
            with pd.ExcelWriter(out1, engine="openpyxl", mode="w") as writer:
                df1_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(
                f"[INFO] Novo arquivo criado e aba 'Classificado' salva: {out1}"
            )
    except Exception as e:
        logging.error(f"[ERRO] Erro ao salvar arquivo {out1}:\n{e}")

    try:
        if os.path.exists(out2):
            with pd.ExcelWriter(
                out2, engine="openpyxl", mode="a", if_sheet_exists="replace"
            ) as writer:
                df2_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(f"[INFO] Aba 'Classificado' salva em: {out2}")
        else:
            with pd.ExcelWriter(out2, engine="openpyxl", mode="w") as writer:
                df2_classificado.to_excel(
                    writer, sheet_name="Classificado", index=False
                )
            print_verde(
                f"[INFO] Novo arquivo criado e aba 'Classificado' salva: {out2}"
            )
    except Exception as e:
        logging.error(f"[ERRO] Erro ao salvar arquivo {out2}:\n{e}")
