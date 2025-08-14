import os
import shutil


def mover_arquivos_por_extensao(diretorio_raiz, pasta_output, extensao_desejada):
    """Move arquivos com uma determinada extensão de um diretório (e seus subdiretórios)
    para uma pasta de saída,"""

    # Normaliza extensão
    if not extensao_desejada.startswith("."):
        extensao_desejada = "." + extensao_desejada
    extensao_desejada = extensao_desejada.lower()

    os.makedirs(pasta_output, exist_ok=True)
    tipos_restantes = {}

    for root, dirs, files in os.walk(diretorio_raiz):
        for file in files:
            extensao = os.path.splitext(file)[1].lower()
            caminho_origem = os.path.join(root, file)

            if extensao == extensao_desejada:
                caminho_destino = os.path.join(pasta_output, file)

                base, ext = os.path.splitext(file)
                contador = 1
                # Evita sobrescrever arquivos repetidos
                while os.path.exists(caminho_destino):
                    caminho_destino = os.path.join(
                        pasta_output, f"{base}_{contador}{ext}"
                    )
                    contador += 1

                shutil.move(caminho_origem, caminho_destino)
                print(f"Movido: {caminho_origem} → {caminho_destino}")
            else:
                chave = extensao if extensao else "[sem extensão]"
                tipos_restantes[chave] = tipos_restantes.get(chave, 0) + 1

    return tipos_restantes
