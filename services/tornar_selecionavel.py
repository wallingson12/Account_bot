import os
import glob
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfMerger
import io

# Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def pdf_to_searchable_pdf(input_pdf_path, output_pdf_path, lang='por'):
    # Converte PDF em imagens (pode ajustar dpi)
    pages = convert_from_path(input_pdf_path, dpi=300)

    merger = PdfMerger()

    for i, page in enumerate(pages):
        # Faz OCR e gera PDF pesquisável da página
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(page, extension='pdf', lang=lang)

        # Carrega o PDF da página em memória
        pdf_stream = io.BytesIO(pdf_bytes)

        # Adiciona a página ao merge
        merger.append(pdf_stream)

        # Libera memória
        page.close()
        pdf_stream.close()

    # Escreve o PDF final no disco
    with open(output_pdf_path, 'wb') as f_out:
        merger.write(f_out)
    merger.close()
    print(f"PDF pesquisável criado: {output_pdf_path}")


if __name__ == "__main__":
    pasta = r"C:\Users\wallingson.silva\Desktop\WALLINGSON\TO DO\Tabulador\files\DCTF"

    # Pega todos os PDFs da pasta
    arquivos_pdf = glob.glob(os.path.join(pasta, "*.pdf"))

    for pdf in arquivos_pdf:
        nome_saida = os.path.join(
            pasta,
            f"pesquisavel_{os.path.basename(pdf)}"
        )
        pdf_to_searchable_pdf(pdf, nome_saida)
