from pathlib import Path

# Configurações fixas
POPPLER_PATH = None  # Ex: r"C:/poppler-xx/bin" se precisar
TESSERACT_CMD_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Pasta de trabalho para leitura e gravação
BASE_PATH = Path(r"C:/Users/wallingson.silva/Desktop/WALLINGSON/TO DO/Aplicação_tabulacao/CFOP")
GABARITO_PATH = BASE_PATH / "gabarito.xlsx"
OUTPUT_PATH = BASE_PATH / "cfop_extraido.xlsx"
