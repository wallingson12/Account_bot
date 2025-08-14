import pandas as pd
import datetime
import time
import requests
import logging

green = "\033[92m"
reset = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(message)s")


def print_verde(msg):
    print(f"{green}{msg}{reset}")


def consulta_cnpj(
    taxa_consulta=3, arquivo_entrada="cnpjs.xlsx", arquivo_saida="resultado_cnpjs.xlsx"
):
    """
    Consulta dados para uma lista de CNPJs no arquivo Excel e salva resultados em outro Excel.
    Controla taxa de consultas para evitar bloqueios.
    """

    try:
        cnpjs_df = pd.read_excel(arquivo_entrada)
    except Exception as e:
        logging.error(f"[ERRO] Falha ao carregar arquivo {arquivo_entrada}: {e}")
        return

    if "CNPJ" not in cnpjs_df.columns:
        logging.error("[ERRO] Coluna 'CNPJ' não encontrada no arquivo de entrada.")
        return

    cnpjs = cnpjs_df["CNPJ"].astype(str).tolist()
    total_cnpjs = len(cnpjs)
    tempo_minutos = total_cnpjs // taxa_consulta
    hora_prevista = datetime.datetime.now() + datetime.timedelta(minutes=tempo_minutos)

    print_verde(
        f"Previsão de tempo para processar {total_cnpjs} CNPJs: {tempo_minutos} minutos"
    )
    print_verde(f"Hora prevista de fim: {hora_prevista.strftime('%H:%M')}")

    resultados = []
    consulta_count = 0

    for cnpj in cnpjs:
        url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logging.error(f"[ERRO] Falha ao consultar CNPJ {cnpj}: {e}")
            continue

        est = data.get("estabelecimento", {})
        optante = data.get("simples", {}).get("simples", "Não")

        inscricao_estadual = "Não informado"
        inscricoes = est.get("inscricoes_estaduais", [])
        estado = est.get("estado", {}).get("nome", "")

        for inscricao in inscricoes:
            if inscricao.get("estado", {}).get("nome") == estado:
                inscricao_estadual = inscricao.get(
                    "inscricao_estadual", "Não informado"
                )
                break

        resultados.append(
            {
                "CNPJ": cnpj,
                "Razão Social": data.get("razao_social", ""),
                "Natureza jurídica descrição": data.get("natureza_juridica", {}).get(
                    "descricao", ""
                ),
                "CEP": est.get("cep", ""),
                "Tipo_logradouro": est.get("tipo_logradouro", ""),
                "logradouro": est.get("logradouro", ""),
                "Bairro": est.get("bairro", ""),
                "numero": est.get("numero", ""),
                "Cidade": est.get("cidade", {}).get("nome", ""),
                "IBGE ID": est.get("cidade", {}).get("ibge_id", ""),
                "Estado": estado,
                "Optante Simples Nacional": optante,
                "Tipo": est.get("tipo", ""),
                "Atividade principal": est.get("atividade_principal", {}).get(
                    "subclasse", ""
                ),
                "Atividade principal descricao": est.get("atividade_principal", {}).get(
                    "descricao", ""
                ),
                "Inscrição estadual": inscricao_estadual,
            }
        )

        consulta_count += 1
        if consulta_count % taxa_consulta == 0:
            print_verde(
                f"Aguardando 60 segundos para respeitar taxa de consulta ({taxa_consulta} por minuto)..."
            )
            time.sleep(60)

    df = pd.DataFrame(resultados)
    try:
        df.to_excel(arquivo_saida, index=False)
        print_verde(f"Processamento concluído! Resultados salvos em {arquivo_saida}")
    except Exception as e:
        logging.error(f"[ERRO] Falha ao salvar arquivo {arquivo_saida}: {e}")
