import os
import re

from pdf2image import convert_from_path
from ocr.ocr import process_image, extract_ocr_data_from_image, config_map
from tabulates.utils.darf_utils import *
from .text_parser_darf import *

def extrair_infos_darf(pdf_path, filename):
    records = []

    # Converte o PDF em imagens (faltava isso)
    images = convert_from_path(pdf_path, dpi=300)

    for page_number, img in enumerate(images, start=1):
        print(f"=== Página {page_number} ===")
        img = img.convert('RGB')

        text, avg_confidence = extract_ocr_data_from_image(img, 'darf', config_map)

        print("\n--- TEXTO OCR COMPLETO ---")
        print(text)
        print("--- FIM DO TEXTO OCR ---\n")
        print(f"📈 Confiança média da página {page_number}: {avg_confidence:.2f}%\n")

        cnpj, razao_social = extract_cnpj_and_razao(text)

        blocks = re.split(r'Data de Vencimento', text)
        if len(blocks) == 1:
            blocks = [text]

        for block in blocks[1:]:
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
                    record = create_record(filename, page_number, cnpj, razao_social, period_start, due_date,
                                           collection_date, document_number, match, reserved_value)
                    if record:
                        records.append(record)

            except Exception as e:
                print(f"[ERRO NA PÁGINA {page_number}] Bloco pulado: {e}")
                continue

    return records

def process_all_pdfs(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    all_records = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"\nProcessando o arquivo: {pdf_file}")
        records = extrair_infos_darf(pdf_path, pdf_file)
        all_records.extend(records)

    return all_records
