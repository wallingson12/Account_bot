import pytesseract

caminho_tesseract = "/usr/bin/tesseract"
pytesseract.pytesseract.tesseract_cmd = caminho_tesseract

def configurar_tesseract(caminho_tesseract):
    pytesseract.pytesseract.tesseract_cmd = caminho_tesseract
