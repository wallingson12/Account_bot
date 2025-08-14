import os
import shutil
import time

# Solicita a pasta base via input
pasta_base = input("Digite o caminho da pasta base: ").strip()

# Solicita os identificadores (separados por vírgula) via input
entrada_identificadores = input("Digite os identificadores separados por vírgula (ex: 201709,201710): ")
identificadores = [ident.strip() for ident in entrada_identificadores.split(',') if ident.strip()]

# Extensões de arquivos Excel
extensoes_excel = {'.xls', '.xlsx', '.xlsm', '.xlsb', '.xltx', '.xltm'}

def mover_arquivo(caminho_arquivo, pasta_xml, pasta_excel, pasta_outros):
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_base, ext = os.path.splitext(nome_arquivo)
    ext = ext.lower()

    if ext == '.xml':
        destino = pasta_xml
    elif ext in extensoes_excel:
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
        print(f'Movido: {os.path.basename(destino_final)} -> {destino}')
    except Exception as e:
        print(f'Erro ao mover {nome_arquivo}: {e}')

# Início da contagem de tempo total
inicio_total = time.time()

# Processa cada identificador
for identificador in identificadores:
    print(f"\n--- Processando identificador: {identificador} ---")

    pasta_origem = os.path.join(pasta_base, identificador)
    pasta_consolidada = os.path.join(pasta_base, f'Consolidadas_{identificador}')
    pasta_xml = os.path.join(pasta_consolidada, "Consolidada XML")
    pasta_excel = os.path.join(pasta_consolidada, "Consolidada Excel")
    pasta_outros = os.path.join(pasta_consolidada, "Consolidada Outros Arquivos")

    # Criação das pastas
    os.makedirs(pasta_xml, exist_ok=True)
    os.makedirs(pasta_excel, exist_ok=True)
    os.makedirs(pasta_outros, exist_ok=True)

    # Início da contagem de tempo individual
    inicio = time.time()

    # Percorre os arquivos da pasta de origem
    for raiz, dirs, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            if not arquivo.lower().endswith('.rar'):
                mover_arquivo(caminho_completo, pasta_xml, pasta_excel, pasta_outros)

    # Fim da contagem de tempo individual
    fim = time.time()
    duracao = (fim - inicio) / 60
    print(f"Concluído para {identificador} em {duracao:.2f} minutos.")

# Fim da contagem total
fim_total = time.time()
duracao_total = (fim_total - inicio_total) / 60
print(f"\nProcesso total concluído em {duracao_total:.2f} minutos!")