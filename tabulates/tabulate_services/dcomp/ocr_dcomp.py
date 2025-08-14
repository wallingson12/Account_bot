import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import numpy as np
import cv2
from config.config import caminho_tesseract

POPPLER_PATH = None  # configure se precisar


def preprocess_dcomp_image(image, width=None, height=None, fx=None, fy=None, keep_aspect=True, interp=cv2.INTER_AREA):
    img_np = np.array(image)

    if width is not None or height is not None or fx is not None or fy is not None:
        h, w = img_np.shape[:2]
        if keep_aspect:
            if width is not None:
                fx = width / float(w)
                fy = fx
            elif height is not None:
                fy = height / float(h)
                fx = fy
        img_np = cv2.resize(
            img_np,
            (width, height) if width and height else None,
            fx=fx,
            fy=fy,
            interpolation=interp
        )

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


def image_to_data_and_text_dcomp(image, lang='por', psm=4, oem=3):
    pytesseract.pytesseract.tesseract_cmd = caminho_tesseract
    config = f'--psm {psm} --oem {oem}'
    ocr_data = pytesseract.image_to_data(image, lang=lang, config=config, output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(image, lang=lang, config=config)
    return ocr_data, text


def calculate_average_confidence_dcomp(ocr_data):
    confidences = [conf for conf in ocr_data['conf'] if isinstance(conf, int) and conf > 0]
    average_confidence = sum(confidences) / len(confidences) if confidences else 0
    return average_confidence


def extract_ocr_data_from_dcomp_image(image):
    processed_img = preprocess_dcomp_image(image)
    ocr_data, text = image_to_data_and_text_dcomp(processed_img)
    average_confidence = calculate_average_confidence_dcomp(ocr_data)
    return text, average_confidence


def pdf_to_dcomp_images(caminho_pdf, dpi=600):
    try:
        if POPPLER_PATH:
            return convert_from_path(str(caminho_pdf), dpi=dpi, poppler_path=POPPLER_PATH)
        else:
            return convert_from_path(str(caminho_pdf), dpi=dpi)
    except Exception as e:
        print(f"❌ Falha ao converter PDF DCOMP '{caminho_pdf}': {e}")
        return []
