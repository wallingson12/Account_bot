import pytesseract
from pdf2image import convert_from_path
import numpy as np
import cv2
from PIL import Image
from pytesseract import Output

POPPLER_PATH = None  # configure se necessário

# Função resize só para redimensionar imagens — sem alterar nada mais
def resize_image(img_np, width=None, height=None, fx=None, fy=None, keep_aspect=True, interp=cv2.INTER_AREA):
    if width is not None or height is not None or fx is not None or fy is not None:
        h, w = img_np.shape[:2]
        if keep_aspect:
            if width is not None:
                fx = width / float(w)
                fy = fx
            elif height is not None:
                fy = height / float(h)
                fx = fy

        if width is not None and height is not None:
            dsize = (int(width), int(height))
            img_np = cv2.resize(img_np, dsize, interpolation=interp)
        elif fx is not None and fy is not None:
            img_np = cv2.resize(img_np, None, fx=fx, fy=fy, interpolation=interp)
        else:
            # Sem parâmetros válidos, retorna a imagem original
            pass
    return img_np

def preprocess_cfop_image(image):
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Corrige canais
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 15, 2
    )
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=3)
    eroded = cv2.erode(dilated, kernel, iterations=2)

    return Image.fromarray(eroded)

def preprocess_darf_image(image):
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Corrige canais
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 15, 2
    )
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=3)
    eroded = cv2.erode(dilated, kernel, iterations=2)

    return Image.fromarray(eroded)

def preprocess_dcomp_image(image):
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Corrige canais
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=2)
    processed_img = Image.fromarray(eroded)
    return processed_img

def preprocess_dctf_image(image):
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Corrige canais
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=2)
    processed_img = Image.fromarray(eroded)
    return processed_img

def preprocess_ocr_fonte_pagadora_image(image):
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Corrige canais
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=2)

    return Image.fromarray(eroded)

def preprocess_ocr_recolhi_image(image):
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Corrige canais
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=2)
    return Image.fromarray(eroded)

def preprocess_tabulate_image(image):
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # Corrige canais
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=2)
    return Image.fromarray(eroded)

# Dicionário com parâmetros padrão para cada tipo
default_params = {
    'cfop':
    {'psm': 4, 'oem': 1, 'lang': 'por'},

    'darf':
    {'psm': 6, 'oem': 1, 'lang': 'por'},

    'dcomp':
    {'psm': 4, 'oem': 3, 'lang': 'por'},

    'dctf':
    {'psm': 4, 'oem': 3, 'lang': 'por'},

    'fonte_pagadora':
    {'psm': 4, 'oem': 3, 'lang': 'por'},

    'recolhi':
    {'psm': 6, 'oem': 3, 'lang': 'por'},

    'free_tabulate':
    {'psm': 6, 'oem': 3, 'lang': 'por'},
}

def image_to_data_and_text(image, psm, oem, lang):
    config = f'--psm {psm} --oem {oem}'
    ocr_data = pytesseract.image_to_data(image, lang=lang, config=config, output_type=Output.DICT)
    text = pytesseract.image_to_string(image, lang=lang, config=config)
    return ocr_data, text

def process_image(image, tipo):
    if tipo not in default_params:
        raise ValueError(f"Tipo '{tipo}' não definido no dicionário de parâmetros.")

    params = default_params[tipo]
    return image_to_data_and_text(image, **params)

def calculate_average_confidence(ocr_data):
    confidences = ocr_data.get('conf', [])
    confidences = [int(c) for c in confidences if str(c).isdigit() and int(c) >= 0]

    if not confidences:
        return 0.0

    average_confidence = sum(confidences) / len(confidences)
    return average_confidence

def extract_ocr_data_from_image(image, ocr_type, config_map):
    funcs = config_map.get(ocr_type)
    if funcs is None:
        raise ValueError(f"OCR type '{ocr_type}' não encontrado no config_map")

    processed_img = funcs['preprocess'](image)
    ocr_data, text = funcs['ocr'](processed_img)
    average_confidence = funcs['confidence'](ocr_data)
    return text, average_confidence

def pdf_to_images(caminho_pdf, dpi=600):
    try:
        if POPPLER_PATH:
            return convert_from_path(str(caminho_pdf), dpi=dpi, poppler_path=POPPLER_PATH)
        else:
            return convert_from_path(str(caminho_pdf), dpi=dpi)
    except Exception as e:
        print(f"❌ Falha ao converter PDF CFOP '{caminho_pdf}': {e}")
        return []

# Mapeamento completo por tipo
config_map = {
    'cfop': {
        'preprocess': preprocess_cfop_image,
        'ocr': lambda img: image_to_data_and_text(img, **default_params['cfop']),
        'confidence': calculate_average_confidence
    },
    'darf': {
        'preprocess': preprocess_darf_image,
        'ocr': lambda img: image_to_data_and_text(img, **default_params['darf']),
        'confidence': calculate_average_confidence
    },
    'dcomp': {
        'preprocess': preprocess_dcomp_image,
        'ocr': lambda img: image_to_data_and_text(img, **default_params['dcomp']),
        'confidence': calculate_average_confidence
    },
    'dctf': {
        'preprocess': preprocess_dctf_image,
        'ocr': lambda img: image_to_data_and_text(img, **default_params['dctf']),
        'confidence': calculate_average_confidence
    },
    'fonte_pagadora': {
        'preprocess': preprocess_ocr_fonte_pagadora_image,
        'ocr': lambda img: image_to_data_and_text(img, **default_params['fonte_pagadora']),
        'confidence': calculate_average_confidence
    },
    'recolhi': {
        'preprocess': preprocess_ocr_recolhi_image,
        'ocr': lambda img: image_to_data_and_text(img, **default_params['recolhi']),
        'confidence': calculate_average_confidence
    },
    'free_tabulate': {
        'preprocess': preprocess_tabulate_image,
        'ocr': lambda img: image_to_data_and_text(img, **default_params['free_tabulate']),
        'confidence': calculate_average_confidence
    },
}
