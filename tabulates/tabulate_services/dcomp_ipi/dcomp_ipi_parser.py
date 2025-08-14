from PyPDF2 import PdfReader
import re

def extrair_texto_pdf_ipi(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        textos = [page.extract_text() for page in reader.pages]
    return textos

def parse_apuracao_ipi(textos, tipo):
    dados = []
    for text in textos:
        if tipo == 'entrada':
            cfop_apura = re.findall(r'CFOP:\s*(\d\.\d{3})', text)
            base_calculo = re.findall(r'Base de Cálculo\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            ipi_creditado = re.findall(r'IPI Creditado\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            isento = re.findall(r'Isentas ou Não Tributadas\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            outros = re.findall(r'Outras\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            for cf, base, ipi_cred, isent, outr in zip(cfop_apura, base_calculo, ipi_creditado, isento, outros):
                dados.append({
                    'CFOP Código': cf,
                    'Base de Cálculo': base,
                    'IPI Creditado': ipi_cred,
                    'Isentas ou Não Tributadas': isent,
                    'Outras': outr
                })
        elif tipo == 'saida':
            cfop_apura = re.findall(r'CFOP:\s*(\d\.\d{3})', text)
            base_calculo = re.findall(r'Base de Cálculo\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            ipi_debitado = re.findall(r'IPI Debitado\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            isento = re.findall(r'Isentas ou Não Tributadas\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            outros = re.findall(r'Outras\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
            for cf, base, ipi_deb, isent, outr in zip(cfop_apura, base_calculo, ipi_debitado, isento, outros):
                dados.append({
                    'CFOP Código': cf,
                    'Base de Cálculo': base,
                    'IPI Debitado': ipi_deb,
                    'Isentas ou Não Tributadas': isent,
                    'Outras': outr
                })
    return dados

def parse_notas_ipi(textos):
    dados = []
    for text in textos:
        cnpj_emitente = re.findall(r'CNPJ do Emitente:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', text)
        notas_fiscais = re.findall(r'N° da Nota Fiscal:\s*(\d+)', text)
        data_emissao = re.findall(r'Data de Emissão:\s*(\d{1,2})/(\s*\d{1,2})/(\d{4})', text)
        data_entrada = re.findall(r'Data de Entrada:\s*(.*)', text)
        cfop = re.findall(r'CFOP:\s*(\d\.\d{3})\s*-\s*(.+)', text)
        total = re.findall(r'Valor Total\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
        valores_ipi = re.findall(r'Valor do IPI Destacado\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)
        valores_ipi_creditado = re.findall(r'Valor do IPI Creditado no Livro RAIPI\s*([\d.,]+(?:\s*-\s*[\d.,]+)?)', text)

        data_emissao = [f"{dia.strip()}/{mes.strip()}/{ano.strip()}" for dia, mes, ano in data_emissao]
        data_entrada = [data.strip() for data in data_entrada]

        max_length = max(len(cnpj_emitente), len(notas_fiscais), len(data_emissao), len(data_entrada), len(cfop),
                         len(total), len(valores_ipi), len(valores_ipi_creditado))

        for i in range(max_length):
            dados.append({
                'CNPJ do Emitente': cnpj_emitente[i] if i < len(cnpj_emitente) else None,
                'N° da Nota Fiscal': notas_fiscais[i] if i < len(notas_fiscais) else None,
                'Data de Emissão': data_emissao[i] if i < len(data_emissao) else None,
                'Data de Entrada': data_entrada[i] if i < len(data_entrada) else None,
                'CFOP Código': cfop[i][0] if i < len(cfop) else None,
                'CFOP Texto': cfop[i][1] if i < len(cfop) else None,
                'Total': total[i] if i < len(total) else None,
                'Valor do IPI Destacado': valores_ipi[i] if i < len(valores_ipi) else None,
                'Valor do IPI Creditado no Livro RAIPI': valores_ipi_creditado[i] if i < len(valores_ipi_creditado) else None
            })
    return dados

def parse_ficha_main_ipi(textos):
    dados = []
    for text in textos:
        processo = re.findall(r'Informado em Processo Administrativo Anterior:\s*(.*)', text)
        informado_outro_perd = re.findall(r'Informado em Outro PER/DCOMP:\s*(.*)', text)
        n_perd_inicial = re.findall(r'N° do PER/DCOMP Inicial:\s*(.*)', text)
        n_perd_ult = re.findall(r'N° do Último PER/DCOMP:\s*(.*)', text)
        credito_sucedida = re.findall(r'Crédito de Sucedida:\s*(\S+)', text)
        situacao_especial = re.findall(r'Situação Especial:\s*(\S+)', text)
        data_evento = re.findall(r'Data do Evento:\s*(\d{2}/\d{2}/\d{4})', text)
        cnpj_credito = re.findall(r'CNPJ do Estabelecimento Detentor do Crédito:\s*(.*)', text)
        trimestre_calendario = re.findall(r'Trimestre-Calendário:\s*(.*)', text)
        matriz_sn = re.findall(r'Estabelecimento tinha condição de Matriz perante o CNPJ no P.A. do Crédito:\s*(\S+)', text)
        matriz_contrib = re.findall(r'Matriz Contribuinte do IPI no Trimestre-Calendário do Crédito:\s*(\S+)', text)
        nao_optante = re.findall(r'Empresa não Optante pelo Simples no Trimestre-Calendário do Crédito:\s*(\S+)', text)
        nao_litigando = re.findall(r'O Contribuinte não está Litigando em Processo Judicial ou Administrativo sobre Matéria que possa Alterar o Valor a ser Ressarcido:\s*(\S+)', text)
        apuracao_decendial = re.findall(r'Apuração Decendial do IPI no Trimestre-Calendário do Crédito:\s*(\S+)', text)
        apuracao_mensal = re.findall(r'Apuração Mensal do IPI no Trimestre-Calendário do Crédito:\s*(\S+)', text)
        micro_epp = re.findall(r'Microempresa ou EPP desenquadrada no Trimestre-Calendário:\s*(\S+)', text)

        dados.append({
            'Processo Administrativo Anterior': processo[0] if processo else None,
            'Informado em Outro PER/DCOMP': informado_outro_perd[0] if informado_outro_perd else None,
            'N° do PER/DCOMP Inicial': n_perd_inicial[0] if n_perd_inicial else None,
            'N° do Último PER/DCOMP': n_perd_ult[0] if n_perd_ult else None,
            'Crédito de Sucedida': credito_sucedida[0] if credito_sucedida else None,
            'Situação Especial': situacao_especial[0] if situacao_especial else None,
            'Data do Evento': data_evento[0] if data_evento else None,
            'CNPJ do Estabelecimento Detentor do Crédito': cnpj_credito[0] if cnpj_credito else None,
            'Trimestre-Calendário': trimestre_calendario[0] if trimestre_calendario else None,
            'Matriz perante o CNPJ no P.A. do Crédito': matriz_sn[0] if matriz_sn else None,
            'Matriz Contribuinte do IPI': matriz_contrib[0] if matriz_contrib else None,
            'Empresa não Optante pelo Simples': nao_optante[0] if nao_optante else None,
            'Não está Litigando': nao_litigando[0] if nao_litigando else None,
            'Apuração Decendial do IPI': apuracao_decendial[0] if apuracao_decendial else None,
            'Apuração Mensal do IPI': apuracao_mensal[0] if apuracao_mensal else None,
            'Microempresa ou EPP desenquadrada': micro_epp[0] if micro_epp else None,
        })
    return dados
