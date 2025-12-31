from lxml import etree
import pandas as pd

"""
Tabulação de arquivos XML de notas fiscais eletrônicas brasileiras.

Este código processa e tabula os seguintes tipos de documentos fiscais eletrônicos:

- NF-e (Nota Fiscal eletrônica) - Modelo 55
- NFC-e (Nota Fiscal de Consumidor eletrônica) - Modelo 65
- CT-e (Conhecimento de Transporte eletrônico) - Modelo 57
- MDF-e (Manifesto eletrônico de Documentos Fiscais) - Modelo 58
"""

def parse_emitente_nfe(root):
    emit = root.find('.//{*}emit')
    if emit is None:
        return {}
    return {
        'emit_CNPJ': emit.findtext('{*}CNPJ'),
        'emit_xNome': emit.findtext('{*}xNome'),
        'emit_xFant': emit.findtext('{*}xFant'),
        'emit_IE': emit.findtext('{*}IE'),
        'emit_Ender': emit.findtext('{*}enderEmit/{*}xLgr')
    }


def parse_destinatario_nfe(root):
    dest = root.find('.//{*}dest')
    if dest is None:
        return {}
    return {
        'dest_CNPJ': dest.findtext('{*}CNPJ') or dest.findtext('{*}CPF'),
        'dest_xNome': dest.findtext('{*}xNome'),
        'dest_IE': dest.findtext('{*}IE'),
        'dest_Ender': dest.findtext('{*}enderDest/{*}xLgr')
    }


def parse_valores_nfe(root):
    total = root.find('.//{*}total/{*}ICMSTot')
    if total is None:
        return {}
    return {
        'vBC': total.findtext('{*}vBC'),
        'vICMS': total.findtext('{*}vICMS'),
        'vICMSDeson': total.findtext('{*}vICMSDeson'),
        'vFCP': total.findtext('{*}vFCP'),
        'vBCST': total.findtext('{*}vBCST'),
        'vST': total.findtext('{*}vST'),
        'vProd': total.findtext('{*}vProd'),
        'vFrete': total.findtext('{*}vFrete'),
        'vSeg': total.findtext('{*}vSeg'),
        'vDesc': total.findtext('{*}vDesc'),
        'vII': total.findtext('{*}vII'),
        'vIPI': total.findtext('{*}vIPI'),
        'vPIS': total.findtext('{*}vPIS'),
        'vCOFINS': total.findtext('{*}vCOFINS'),
        'vOutro': total.findtext('{*}vOutro'),
        'vNF': total.findtext('{*}vNF')
    }


def parse_itens_nfe(root):
    itens = []
    dets = root.findall('.//{*}det')
    for det in dets:
        prod = det.find('{*}prod')
        imposto = det.find('{*}imposto')
        if prod is None:
            continue
        item = {
            'nItem': det.get('nItem'),
            'cProd': prod.findtext('{*}cProd'),
            'xProd': prod.findtext('{*}xProd'),
            'cfop': prod.findtext('{*}cfop'),
            'uCom': prod.findtext('{*}uCom'),
            'qCom': prod.findtext('{*}qCom'),
            'vUnCom': prod.findtext('{*}vUnCom'),
            'vProd': prod.findtext('{*}vProd'),
        }

        # Exemplo básico de imposto ICMS
        icms = imposto.find('{*}ICMS')
        if icms is not None:
            icms_child = next(iter(icms))  # Exemplo: ICMS00, ICMS10 etc
            item['ICMS_CST'] = icms_child.findtext('{*}CST') or icms_child.findtext('{*}cst')
            item['ICMS_vICMS'] = icms_child.findtext('{*}vICMS')
        else:
            item['ICMS_CST'] = None
            item['ICMS_vICMS'] = None

        itens.append(item)
    return pd.DataFrame(itens)


def parse_nfe(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # Dados gerais
    infNFe = root.find('.//{*}infNFe')
    if infNFe is None:
        raise ValueError("XML inválido para NF-e")

    dados = {
        'chNFe': infNFe.get('Id').replace('NFe', '') if infNFe.get('Id') else None,
        'ide_nNF': infNFe.findtext('{*}ide/{*}nNF'),
        'ide_dhEmi': infNFe.findtext('{*}ide/{*}dhEmi') or infNFe.findtext('{*}ide/{*}dEmi'),
        'ide_tpNF': infNFe.findtext('{*}ide/{*}tpNF'),
        'ide_mod': infNFe.findtext('{*}ide/{*}mod'),
    }
    dados.update(parse_emitente_nfe(infNFe))
    dados.update(parse_destinatario_nfe(infNFe))
    dados.update(parse_valores_nfe(infNFe))

    df_geral = pd.DataFrame([dados])
    df_itens = parse_itens_nfe(infNFe)

    return df_geral, df_itens


# Para NFC-e, estrutura é parecida da NF-e, apenas algumas tags diferentes.
def parse_nfce(xml_path):
    # Para simplificar, chamamos parse_nfe (muitas vezes são iguais).
    return parse_nfe(xml_path)


def parse_cte(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    infCTe = root.find('.//{*}infCTe')
    if infCTe is None:
        raise ValueError("XML inválido para CT-e")

    dados = {
        'chCTe': infCTe.get('Id').replace('CTe', '') if infCTe.get('Id') else None,
        'ide_dhEmi': infCTe.findtext('{*}ide/{*}dhEmi'),
        'ide_mod': infCTe.findtext('{*}ide/{*}mod'),
    }

    # Emitente (remetente)
    emit = infCTe.find('{*}emit')
    dados.update({
        'emit_CNPJ': emit.findtext('{*}CNPJ') if emit is not None else None,
        'emit_xNome': emit.findtext('{*}xNome') if emit is not None else None,
    })

    # Destinatário (tomador)
    dest = infCTe.find('{*}dest')
    dados.update({
        'dest_CNPJ': dest.findtext('{*}CNPJ') if dest is not None else None,
        'dest_xNome': dest.findtext('{*}xNome') if dest is not None else None,
    })

    # Valores
    vPrest = infCTe.find('{*}vPrest')
    if vPrest is not None:
        dados['vPrest_vTPrest'] = vPrest.findtext('{*}vTPrest')
        dados['vPrest_vRec'] = vPrest.findtext('{*}vRec')

    # Itens do CT-e (serviços de transporte)
    itens = []
    infServ = infCTe.find('{*}infServico')
    if infServ is not None:
        item = {
            'xDescServ': infServ.findtext('{*}xDescServ'),
            'vServ': infServ.findtext('{*}vServ'),
            'vCarga': infServ.findtext('{*}vCarga'),
        }
        itens.append(item)

    df_geral = pd.DataFrame([dados])
    df_itens = pd.DataFrame(itens)

    return df_geral, df_itens


def parse_mdfe(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    infMDFe = root.find('.//{*}infMDFe')
    if infMDFe is None:
        raise ValueError("XML inválido para MDF-e")

    dados = {
        'chMDFe': infMDFe.get('Id').replace('MDFe', '') if infMDFe.get('Id') else None,
        'ide_dhEmi': infMDFe.findtext('{*}ide/{*}dhEmi'),
        'ide_mod': infMDFe.findtext('{*}ide/{*}mod'),
    }

    emit = infMDFe.find('{*}emit')
    dados.update({
        'emit_CNPJ': emit.findtext('{*}CNPJ') if emit is not None else None,
        'emit_xNome': emit.findtext('{*}xNome') if emit is not None else None,
    })

    # Itens MDF-e (documentos relacionados)
    itens = []
    docs = infMDFe.findall('.//{*}infDoc')
    for doc in docs:
        item = {
            'tipoDoc': doc.findtext('{*}tpDoc'),
            'serie': doc.findtext('{*}serie'),
            'nDoc': doc.findtext('{*}nDoc'),
            'dtDoc': doc.findtext('{*}dtDoc'),
        }
        itens.append(item)

    df_geral = pd.DataFrame([dados])
    df_itens = pd.DataFrame(itens)

    return df_geral, df_itens


def detectar_tipo_e_parser(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()
    ns_uri = etree.QName(root).namespace or ""
    tag = etree.QName(root).localname

    # Detecta pelo tag raiz e namespace
    if tag == 'NFe':
        return parse_nfe
    elif tag == 'CTe':
        return parse_cte
    elif tag == 'MDFe':
        return parse_mdfe
    elif tag == 'nfeProc':
        # Documento NF-e encapsulado
        return parse_nfe
    elif tag == 'NFCe':
        # Nota fiscal consumidor eletrônica
        return parse_nfce
    else:
        raise ValueError(f"Tipo de XML não suportado: {tag}")


def parse_xml(xml_path):
    parser = detectar_tipo_e_parser(xml_path)
    return parser(xml_path)


if __name__ == "__main__":
    import sys
    arquivo_xml = sys.argv[1]
    df_geral, df_itens = parse_xml(arquivo_xml)

    print("### DADOS GERAIS ###")
    print(df_geral.to_string(index=False))
    print("\n### ITENS ###")
    print(df_itens.to_string(index=False))