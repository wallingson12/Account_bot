import re
from pathlib import Path
import PyPDF2
import pandas as pd

# Caminhos base
BASE_DIR = Path(r"C:\Users\wallingson.silva\Downloads\CHAMADOS\FINANCIAL SERVICES\duplicatas\duplicatas")
OUTPUT_PATH = BASE_DIR / "nf" / "notas_fiscais_extraidas.xlsx"

def extrair_texto_pdf(caminho_pdf: Path) -> str:
    """Extrai o texto de um PDF."""
    texto_extraido = ""
    with caminho_pdf.open("rb") as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        for pagina in leitor.pages:
            texto_extraido += pagina.extract_text() or ""
    return texto_extraido

def extrair_campo(texto: str, chave: str, padrao_valor: str) -> str:
    """Busca um campo com regex na mesma linha ou na próxima linha."""
    padroes = [
        rf"{chave}\s*[:\-]?\s*({padrao_valor})",         # mesma linha
        rf"{chave}\s*\n\s*({padrao_valor})",             # próxima linha
    ]
    for padrao in padroes:
        if match := re.search(padrao, texto, re.IGNORECASE):
            return match.group(1).strip()
    return ""

def limpar_municipio_bloco(linha: str) -> str:
    """Remove parte 'UF' da linha de município, se presente."""
    return re.split(r"\bUF\b", linha.strip())[0].strip()

def extrair_dados_nfe(texto: str) -> tuple[dict, list[dict]]:
    """Extrai campos e produtos da NF-e a partir do texto."""
    dados = {
        "Chave": extrair_campo(texto, "Chave de Acesso", r"[\d./\-]+"),
        "numero_nfe": extrair_campo(texto, r"N[úu]mero NF-e", r"\d+"),
        "natureza": "",
        "tipo_operacao": "",
        "modelo": extrair_campo(texto, "Modelo", r"\d+"),
        "serie": extrair_campo(texto, "Série", r"\d+"),
        "data": extrair_campo(texto, "Data/Hora da emissão", r"\d{2}/\d{2}/\d{4}"),
        "emitente_cnpj": "",
        "emitente_razao_social": "",
        "emitente_municipio": "",
        "emitente_uf": extrair_campo(texto, "UF", r"[A-Z]{2}"),
        "destinatario_cnpj": "",
        "destinatario_razao_social": "",
        "destinatario_municipio": "",
        "destinatario_uf": "",
    }

    # Natureza e Tipo da operação
    if match := re.search(r"Natureza da operação\s*\n(.*?)\s*Tipo da operação", texto, re.DOTALL | re.IGNORECASE):
        dados["natureza"] = " ".join(match.group(1).split())
    else:
        dados["natureza"] = extrair_campo(texto, "Natureza da operação", r"[^\n]+")

    if match := re.search(r"Tipo da operação\s*\n(.*?)(?=\s*Chave)", texto, re.DOTALL | re.IGNORECASE):
        dados["tipo_operacao"] = " ".join(match.group(1).split())
    else:
        dados["tipo_operacao"] = extrair_campo(texto, "Tipo da operação", r"[^\n]+")

    # Emitente CNPJ
    if match := re.search(r"Emitente\s*CNPJ\s*\n([\d./\-\n\s]+?)IE", texto, re.IGNORECASE):
        dados["emitente_cnpj"] = re.sub(r"[\s\n]", "", match.group(1)).strip()
    else:
        dados["emitente_cnpj"] = extrair_campo(texto, r"Emitente\s*CNPJ", r"[\d./\-]+")

    # Destinatário CNPJ
    padroes_dest_cnpj = [
        r"Destinat[áa]rio\s*CNPJ\s*[:\-]?\s*([\d./\-]+)",
        r"Destinat[áa]rio\s*CNPJ\s*\n\s*([\d./\-]+)(?!\n\s*IE)"
    ]
    for padrao in padroes_dest_cnpj:
        if match := re.search(padrao, texto, re.IGNORECASE):
            dados["destinatario_cnpj"] = match.group(1).strip()
            break

    # Razões sociais
    razoes_sociais = re.findall(r"Nome/Raz[aã]o Social\s*\n([^\n]+)", texto)
    if len(razoes_sociais) >= 1:
        dados["emitente_razao_social"] = razoes_sociais[0].strip()
    if len(razoes_sociais) >= 2:
        dados["destinatario_razao_social"] = razoes_sociais[1].strip()

    # Municípios
    municipios = re.findall(r"Munic[ií]pio\s*\n([^\n]+)", texto)
    if len(municipios) >= 1:
        dados["emitente_municipio"] = limpar_municipio_bloco(municipios[0])
    if len(municipios) >= 2:
        dados["destinatario_municipio"] = limpar_municipio_bloco(municipios[1])

    # UF destinatário
    ufs = re.findall(r"UF\s*\n([A-Z]{2})", texto)
    if len(ufs) >= 2:
        dados["destinatario_uf"] = ufs[1].strip()

    # Produtos
    produtos = []
    if match := re.search(r"Produtos\s*\n((?:.+\n)+?)(?:Valor total|Eventos|$)", texto, re.IGNORECASE):
        linhas = match.group(1).strip().splitlines()
        for linha in linhas:
            if re.search(r"Descrição|Quantidade|Unid\.|Valor\s*Unit\.|Valor\s*Prod\.", linha, re.IGNORECASE):
                continue
            partes = linha.split()
            if len(partes) >= 5:
                produtos.append({
                    "produto": partes[0],
                    "quantidade": partes[1].replace(",", "."),
                    "unidade": partes[2],
                    "valor_uni": partes[3].replace(".", "").replace(",", "."),
                    "valor_prod": partes[4].replace(".", "").replace(",", "."),
                })

    return dados, produtos

def processar_pdfs_em_diretorio(diretorio: Path) -> pd.DataFrame:
    """Processa todos os PDFs em um diretório e retorna DataFrame com dados extraídos."""
    registros = []

    for pdf in diretorio.glob("*.pdf"):
        print(f"Processando: {pdf.name}")
        texto = extrair_texto_pdf(pdf)
        dados_nfe, produtos = extrair_dados_nfe(texto)

        for prod in produtos:
            registro = {"arquivo": pdf.name}
            registro.update(dados_nfe)
            registro.update(prod)
            registros.append(registro)

    df = pd.DataFrame(registros)
    if not df.empty and "arquivo" in df.columns:
        df = df[["arquivo"] + [col for col in df.columns if col != "arquivo"]]

    return df

def salvar_em_excel(df: pd.DataFrame, caminho_saida: Path):
    """Salva o DataFrame em um arquivo Excel."""
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(caminho_saida, index=False)
    print(f"Arquivo salvo em: {caminho_saida}")

if __name__ == "__main__":
    df_nfes = processar_pdfs_em_diretorio(BASE_DIR)
    salvar_em_excel(df_nfes, OUTPUT_PATH)
