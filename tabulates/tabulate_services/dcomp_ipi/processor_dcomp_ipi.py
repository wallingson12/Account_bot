import pandas as pd
from .dcomp_ipi_parser import extrair_texto_pdf_ipi, parse_apuracao_ipi, parse_notas_ipi, parse_ficha_main_ipi

def processor_dcomp_ipi(caminho_arquivo, dados_apuracao_entrada, dados_apuracao_saida, dados_notas, dados_ficha_main):
    with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
        if dados_apuracao_entrada:
            pd.DataFrame(dados_apuracao_entrada).to_excel(writer, sheet_name='Apuração IPI Entrada', index=False)
        if dados_apuracao_saida:
            pd.DataFrame(dados_apuracao_saida).to_excel(writer, sheet_name='Apuração IPI Saída', index=False)
        if dados_notas:
            pd.DataFrame(dados_notas).to_excel(writer, sheet_name='Ficha Notas Fiscais', index=False)
        if dados_ficha_main:
            pd.DataFrame(dados_ficha_main).to_excel(writer, sheet_name='Ficha Principal', index=False)

def dcomp_ipi(pdf_path, caminho_arquivo_saida):
    textos = extrair_texto_pdf_ipi(pdf_path)
    dados_apuracao_entrada = parse_apuracao_ipi(textos, 'entrada')
    dados_apuracao_saida = parse_apuracao_ipi(textos, 'saida')
    dados_notas = parse_notas_ipi(textos)
    dados_ficha_main = parse_ficha_main_ipi(textos)
    processor_dcomp_ipi(caminho_arquivo_saida, dados_apuracao_entrada, dados_apuracao_saida, dados_notas, dados_ficha_main)