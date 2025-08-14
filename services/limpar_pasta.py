import os
import logging


def limpar_arquivos_por_formato(pasta_raiz, formato_manter):
    """
    Remove arquivos dentro de pasta_raiz que não possuem a extensão formato_manter.

    :param pasta_raiz: caminho da pasta para limpeza
    :param formato_manter: extensão dos arquivos que devem ser mantidos (ex: 'pdf', '.txt')
    """
    if not os.path.isdir(pasta_raiz):
        logging.error(f"Pasta inválida: {pasta_raiz}")
        return

    formato_manter = formato_manter.lower()
    if not formato_manter.startswith("."):
        formato_manter = "." + formato_manter

    total_removidos = 0
    for root, _, files in os.walk(pasta_raiz):
        for file in files:
            if os.path.splitext(file)[1].lower() != formato_manter:
                caminho = os.path.join(root, file)
                try:
                    os.remove(caminho)
                    logging.info(f"Arquivo removido: {caminho}")
                    total_removidos += 1
                except Exception as e:
                    logging.error(f"Erro ao remover {caminho}: {e}")

    logging.info(
        f"Processo de limpeza concluído. Total de arquivos removidos: {total_removidos}"
    )
