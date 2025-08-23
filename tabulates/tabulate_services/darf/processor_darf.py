from ocr.ocr import extract_ocr_data_from_image, config_map
from .text_parser_darf import *

import re
import pdfplumber
from pdf2image import convert_from_path

def extrair_infos_darf(pdf_path, filename, usar_ocr=False):
    records = []

    if usar_ocr:
        images = convert_from_path(pdf_path, dpi=500)
        for page_number, img in enumerate(images, start=1):
            print(f"=== Página {page_number} ===")
            img = img.convert('RGB')

            text, avg_confidence = extract_ocr_data_from_image(img, 'darf', config_map)

            print("\n--- TEXTO OCR COMPLETO ---")
            print(text)
            print("--- FIM DO TEXTO OCR ---\n")
            print(f"📈 Confiança média da página {page_number}: {avg_confidence:.2f}%\n")

            records.extend(process_darf_text(text, filename, page_number))
    else:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                print(f"=== Página {page_number} === (sem OCR)")
                text = page.extract_text() or ""
                print(text)
                records.extend(process_darf_text(text, filename, page_number))

    return records


def process_darf_text(text, filename, page_number):
    records = []

    cnpj, razao_social = extract_cnpj_and_razao(text)

    blocks = re.split(r'Data de Vencimento', text)
    if len(blocks) <= 1:
        blocks = [text]
    else:
        blocks = blocks[1:]

    for block in blocks:
        try:
            lines = [line.strip() for line in block.strip().splitlines() if line.strip()]

            period_match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s+([\d/]+)', block)
            if period_match:
                period_start = period_match.group(1)
                due_date = period_match.group(2)
                document_number = clean_document_number(period_match.group(3).replace('/', '').strip())
            else:
                period_start = due_date = document_number = None

            reserved_value_match = re.search(r'Valor Reservado/Restituído\s+([\d.,]+)', block)
            reserved_value = reserved_value_match.group(1) if reserved_value_match else '0,00'

            collection_date = extract_collection_date(lines)

            matches = re.findall(
                r'(\d{4})\s+(.+?)\s+([\d.,\-–]+)\s+([\d.,\-–]+)\s+([\d.,\-–]+)\s+([\d.,\-–]+)',
                block
            )

            for match in matches:
                record = create_record(
                    filename, page_number, cnpj, razao_social,
                    period_start, due_date, collection_date,
                    document_number, match, reserved_value
                )
                if record:
                    records.append(record)

        except Exception as e:
            print(f"[ERRO NA PÁGINA {page_number}] Bloco pulado: {e}")
            continue

    return records