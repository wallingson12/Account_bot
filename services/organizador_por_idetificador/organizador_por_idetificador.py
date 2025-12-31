# services/organizador_por_identificador/organizador_por_identificador.py

import os
import shutil

# Extensões de arquivos Excel
EXTENSOES_EXCEL = {'.xls', '.xlsx', '.xlsm', '.xlsb', '.xltx', '.xltm'}

def mover_arquivos_por_extensao(caminho_arquivo, pasta_xml, pasta_excel, pasta_outros):
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_base, ext = os.path.splitext(nome_arquivo)
    ext = ext.lower()

    if ext == '.xml':
        destino = pasta_xml
    elif ext in EXTENSOES_EXCEL:
        destino = pasta_excel
    else:
        destino = pasta_outros

    destino_final = os.path.join(destino, nome_arquivo)
    contador = 1
    while os.path.exists(destino_final):
        novo_nome = f"{nome_base}({contador}){ext}"
        destino_final = os.path.join(destino, novo_nome)
        contador += 1

    try:
        shutil.move(caminho_arquivo, destino_final)
        print(f'Movido: {nome_arquivo} -> {destino}')
    except Exception as e:
        print(f'Erro ao mover {nome_arquivo}: {e}')

# Função principal para rodar diretamente
def organizar_por_identificador(pasta_base, identificadores):
    import time
    inicio_total = time.time()

    for identificador in identificadores:
        pasta_origem = os.path.join(pasta_base, identificador)
        pasta_consolidada = os.path.join(pasta_base, f'Consolidadas_{identificador}')
        pasta_xml = os.path.join(pasta_consolidada, "Consolidada XML")
        pasta_excel = os.path.join(pasta_consolidada, "Consolidada Excel")
        pasta_outros = os.path.join(pasta_consolidada, "Consolidada Outros Arquivos")

        os.makedirs(pasta_xml, exist_ok=True)
        os.makedirs(pasta_excel, exist_ok=True)
        os.makedirs(pasta_outros, exist_ok=True)

        for raiz, dirs, arquivos in os.walk(pasta_origem):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                if not arquivo.lower().endswith('.rar'):
                    mover_arquivos_por_extensao(caminho_completo, pasta_xml, pasta_excel, pasta_outros)

    fim_total = time.time()
    print(f"Processo total concluído em {(fim_total - inicio_total)/60:.2f} minutos!")

# Executa somente se rodar diretamente
if __name__ == "__main__":
    pasta_base = input("Digite o caminho da pasta base: ").strip()
    entrada_identificadores = input("Digite os identificadores separados por vírgula (ex: 201709,201710): ")
    identificadores = [ident.strip() for ident in entrada_identificadores.split(',') if ident.strip()]
    organizar_por_identificador(pasta_base, identificadores)
