from PIL import Image
from pdf2image import convert_from_path
from ocr.ocr import config_map, extract_ocr_data_from_image
import numpy as np

# Função de avaliação continua igual
def avaliar_qualidade_ocr_image(image, ocr_type):
    if ocr_type not in config_map:
        raise ValueError(f"Tipo de OCR '{ocr_type}' não definido no config_map.")

    # Extrai dados OCR da imagem processada
    text, _ = extract_ocr_data_from_image(image, ocr_type, config_map)
    print(text)
    ocr_data, _ = config_map[ocr_type]['ocr'](config_map[ocr_type]['preprocess'](image))

    # Avalia a qualidade
    palavras = [t for t in ocr_data['text'] if t.strip()]
    confs = [
        float(c) for c, t in zip(ocr_data['conf'], ocr_data['text'])
        if c != '-1' and t.strip()
    ]

    total_palavras = len(palavras)
    palavras_confiaveis = sum(1 for c in confs if c >= 80)
    palavras_ruins = sum(1 for c in confs if c < 50)
    media_conf = np.mean(confs) if confs else 0
    tamanho_medio_palavra = np.mean([len(p) for p in palavras]) if palavras else 0
    percentual_boas = (palavras_confiaveis / total_palavras) * 100 if total_palavras > 0 else 0

    return {
        "confiança_média": round(media_conf, 2),
        "total_palavras": total_palavras,
        "palavras_confiáveis (≥80)": palavras_confiaveis,
        "palavras_muito_ruins (<50)": palavras_ruins,
        "tamanho_médio_palavra": round(tamanho_medio_palavra, 2),
        "percentual_palavras_boas": round(percentual_boas, 2)
    }

# Converte PDF em imagens
pdf_path = r"/home/wallingson/Github/Account_bot-main/files/DARF/Lote 1.pdf"
pages = convert_from_path(pdf_path, dpi=300)  # cada página vira uma imagem PIL

# Avalia OCR em cada página
for i, page in enumerate(pages, start=1):
    resultado = avaliar_qualidade_ocr_image(page, "darf")
    print(f"Página {i}: {resultado}")
