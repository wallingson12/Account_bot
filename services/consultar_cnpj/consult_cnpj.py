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
    contador_consultas = 0

    for cnpj in cnpjs:
        url = f"https://publica.cnpj.ws/cnpj/{cnpj}"

        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()

            try:
                data = resp.json()
            except ValueError:
                logging.error(f"[ERRO] Resposta não é JSON para CNPJ {cnpj}")
                continue

            if not isinstance(data, dict):
                logging.error(f"[ERRO] Resposta inválida ou nula para CNPJ {cnpj}")
                continue

        except Exception as e:
            logging.error(f"[ERRO] Falha ao consultar CNPJ {cnpj}: {e}")
            continue

        estabelecimento = data.get("estabelecimento") or {}
        simples = data.get("simples") or {}
        optante_simples = simples.get("simples", "Não")

        inscricao_estadual = "Não informado"
        inscricoes = estabelecimento.get("inscricoes_estaduais") or []
        estado = (estabelecimento.get("estado") or {}).get("nome", "")

        for inscricao in inscricoes:
            if (inscricao.get("estado") or {}).get("nome") == estado:
                inscricao_estadual = inscricao.get(
                    "inscricao_estadual", "Não informado"
                )
                break

        resultados.append(
            {
                "CNPJ": cnpj,
                "Razão Social": data.get("razao_social", ""),
                "Natureza jurídica descrição": (data.get("natureza_juridica") or {}).get(
                    "descricao", ""
                ),
                "CEP": estabelecimento.get("cep", ""),
                "Tipo_logradouro": estabelecimento.get("tipo_logradouro", ""),
                "logradouro": estabelecimento.get("logradouro", ""),
                "Bairro": estabelecimento.get("bairro", ""),
                "numero": estabelecimento.get("numero", ""),
                "Cidade": (estabelecimento.get("cidade") or {}).get("nome", ""),
                "IBGE ID": (estabelecimento.get("cidade") or {}).get("ibge_id", ""),
                "Estado": estado,
                "Optante Simples Nacional": optante_simples,
                "Tipo": estabelecimento.get("tipo", ""),
                "Atividade principal": (estabelecimento.get("atividade_principal") or {}).get(
                    "subclasse", ""
                ),
                "Atividade principal descricao": (estabelecimento.get("atividade_principal") or {}).get(
                    "descricao", ""
                ),
                "Inscrição estadual": inscricao_estadual,
            }
        )

        contador_consultas += 1
        if contador_consultas % taxa_consulta == 0:
            print_verde(
                f"Aguardando 60 segundos para respeitar taxa de consulta ({taxa_consulta} por minuto)..."
            )
            time.sleep(60)

    df = pd.DataFrame(resultados)

    if df.empty:
        logging.error("[ERRO] Nenhum resultado válido para salvar.")
        return

    try:
        df.to_excel(arquivo_saida, index=False)
        print_verde(f"Processamento concluído! Resultados salvos em {arquivo_saida}")
    except Exception as e:
        logging.error(f"[ERRO] Falha ao salvar arquivo {arquivo_saida}: {e}")
