import os
import shutil
import xml.etree.ElementTree as ET

def mover_arquivos_xml_metade(pasta_base, pasta_destino, dividir=False):

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    if dividir:
        # Pega só arquivos XML na pasta base, sem subpastas
        arquivos = [f for f in os.listdir(pasta_base) if f.lower().endswith(".xml")]
        quantidade_para_mover = len(arquivos) // 2

        for arquivo in arquivos[:quantidade_para_mover]:
            origem = os.path.join(pasta_base, arquivo)
            destino = os.path.join(pasta_destino, arquivo)
            try:
                shutil.move(origem, destino)
                print(f"{arquivo} movido para {pasta_destino}")
            except Exception as e:
                print(f"Erro ao mover {arquivo}: {e}")

        print(f"{quantidade_para_mover} arquivos movidos para {pasta_destino}")
    else:
        # Mover todos os arquivos XML recursivamente
        for raiz, _, arquivos in os.walk(pasta_base):
            for arquivo in arquivos:
                if arquivo.lower().endswith(".xml"):
                    origem = os.path.join(raiz, arquivo)
                    destino = os.path.join(pasta_destino, arquivo)
                    try:
                        shutil.move(origem, destino)
                        print(f"{arquivo} movido para {pasta_destino}")
                    except Exception as e:
                        print(f"Erro ao mover {arquivo}: {e}")


def organizar_xml_por_data(diretorio, organizar_por="ano"):
    """
    Organiza arquivos XML no diretório dado, criando subpastas por 'ano' ou 'mes/ano' baseados no dhEmi do XML.
    :param diretorio: pasta onde estão os XMLs
    :param organizar_por: 'ano' ou 'mes/ano'
    """

    def extrair_dhEmi(xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            dhEmi = root.find(".//dEmi")
            if dhEmi is not None:
                return dhEmi.text
            # Tentativa de encontrar tags similares
            for elem in root.iter():
                if "perApur" in elem.tag:
                    return elem.text
                if any(x in elem.tag for x in ("dhEmi", "dEmi", "dhEvento")):
                    return elem.text
            return None
        except ET.ParseError as e:
            print(f"Erro ao analisar {xml_file}: {e}")
            return None

    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(".xml"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            data_emissao = extrair_dhEmi(caminho_arquivo)
            if not data_emissao:
                print(f"Arquivo: {arquivo} - dhEmi não encontrado")
                continue

            if organizar_por == "ano":
                pasta_destino = os.path.join(diretorio, data_emissao[:4])
            elif organizar_por == "mes/ano":
                pasta_destino = os.path.join(
                    diretorio, f"{data_emissao[5:7]}-{data_emissao[:4]}"
                )
            else:
                print(
                    f"Organização '{organizar_por}' inválida. Use 'ano' ou 'mes/ano'."
                )
                return

            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)

            shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))
            print(f"Movido {arquivo} para {pasta_destino}")
