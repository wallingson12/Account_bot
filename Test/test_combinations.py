# param_grid = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": [None, "otsu", "adaptive", "binary", "binary_inv", "trunc", "tozero", "tozero_inv"],
#     "invert": [False, True],
#     "equalize": [False, True],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],#iluminação
#     "clahe_tile": [(8, 8), (16, 16)], #equalização
#     "blur": [None, "median", "gaussian"],
#     "median_ksize": [3, 5, 7],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }

import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract
import optuna
import json
import logging

# Definindo o caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
# Caminho da pasta com arquivos PDF
pdf_folder = r"/home/wallingson/Github/Account_bot-main/files/DCTF"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

param_grid_1 = {
    "grayscale": [True],
    "resize": [1.0, 1.5, 2.0],
    "threshold": ["adaptive"],
    "invert": [False, True],
    "equalize": [False],
    "clahe": [False, True],
    "clahe_clip": [1.0, 2.0, 3.0],
    "clahe_tile": [(8, 8), (16, 16)],
    "blur": ["median"],
    "median_ksize": [3, 5, 7],
    "gaussian_ksize": [None],
    "gaussian_sigma": [None],
    "bilateral": [False, True],
    "bilateral_diameter": [5, 9],
    "bilateral_sigma_color": [75, 150],
    "bilateral_sigma_space": [75, 150],
    "sharpen": [False, True],
    "dilate": [0, 1, 2, 3],
    "erode": [0, 1, 2, 3],
    "morph_open": [0, 1, 2],
    "morph_close": [0, 1, 2],
    "morph_kernel": [(3, 3), (5, 5)],
    "morph_iterations": [1, 2],
}

# param_grid_2 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["otsu"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["median"],
#     "median_ksize": [3, 5, 7],
#     "gaussian_ksize": [None],
#     "gaussian_sigma": [None],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_3 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["binary"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["median"],
#     "median_ksize": [3, 5, 7],
#     "gaussian_ksize": [None],
#     "gaussian_sigma": [None],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_4 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["binary_inv"],
#     "invert": [False],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["median"],
#     "median_ksize": [3, 5, 7],
#     "gaussian_ksize": [None],
#     "gaussian_sigma": [None],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_5 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["trunc"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["median"],
#     "median_ksize": [3, 5, 7],
#     "gaussian_ksize": [None],
#     "gaussian_sigma": [None],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_6 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["tozero"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["median"],
#     "median_ksize": [3, 5, 7],
#     "gaussian_ksize": [None],
#     "gaussian_sigma": [None],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_7 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["tozero_inv"],
#     "invert": [False],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["median"],
#     "median_ksize": [3, 5, 7],
#     "gaussian_ksize": [None],
#     "gaussian_sigma": [None],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# # Agora os 7 restantes com "blur": "gaussian":
#
# param_grid_8 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["adaptive"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["gaussian"],
#     "median_ksize": [None],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_9 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["otsu"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["gaussian"],
#     "median_ksize": [None],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_10 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["binary"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["gaussian"],
#     "median_ksize": [None],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_11 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["binary_inv"],
#     "invert": [False],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["gaussian"],
#     "median_ksize": [None],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_12 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["trunc"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["gaussian"],
#     "median_ksize": [None],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_13 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["tozero"],
#     "invert": [False, True],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["gaussian"],
#     "median_ksize": [None],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }
#
# param_grid_14 = {
#     "grayscale": [True],
#     "resize": [1.0, 1.5, 2.0],
#     "threshold": ["tozero_inv"],
#     "invert": [False],
#     "equalize": [False],
#     "clahe": [False, True],
#     "clahe_clip": [1.0, 2.0, 3.0],
#     "clahe_tile": [(8, 8), (16, 16)],
#     "blur": ["gaussian"],
#     "median_ksize": [None],
#     "gaussian_ksize": [(3, 3), (5, 5)],
#     "gaussian_sigma": [0.5, 1.0],
#     "bilateral": [False, True],
#     "bilateral_diameter": [5, 9],
#     "bilateral_sigma_color": [75, 150],
#     "bilateral_sigma_space": [75, 150],
#     "sharpen": [False, True],
#     "dilate": [0, 1, 2, 3],
#     "erode": [0, 1, 2, 3],
#     "morph_open": [0, 1, 2],
#     "morph_close": [0, 1, 2],
#     "morph_kernel": [(3, 3), (5, 5)],
#     "morph_iterations": [1, 2],
# }

def pdf_to_images(pdf_path, dpi=300):
    images = convert_from_path(pdf_path, dpi=dpi)
    return images


def apply_threshold(img, thresh_type, invert):
    if thresh_type is None:
        return img

    if thresh_type == "adaptive":
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY,
                                     11, 2)
    elif thresh_type == "otsu":
        flag = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU if invert else cv2.THRESH_BINARY + cv2.THRESH_OTSU
        _, thresh_img = cv2.threshold(img, 0, 255, flag)
        return thresh_img
    elif thresh_type == "binary":
        flag = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
        _, thresh_img = cv2.threshold(img, 127, 255, flag)
        return thresh_img
    elif thresh_type == "binary_inv":
        _, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
        return thresh_img
    elif thresh_type == "trunc":
        _, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
        return cv2.bitwise_not(thresh_img) if invert else thresh_img
    elif thresh_type == "tozero":
        _, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
        return cv2.bitwise_not(thresh_img) if invert else thresh_img
    elif thresh_type == "tozero_inv":
        _, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
        return cv2.bitwise_not(thresh_img) if invert else thresh_img
    else:
        return img


def preprocess_image(pil_img, params):
    img = np.array(pil_img)

    # Grayscale
    if params["grayscale"]:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize
    scale = params["resize"]
    if scale != 1.0:
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

    # Equalize histogram (requires grayscale)
    if params["equalize"]:
        img = cv2.equalizeHist(img)

    # CLAHE (requires grayscale)
    if params["clahe"]:
        clahe = cv2.createCLAHE(clipLimit=params["clahe_clip"], tileGridSize=params["clahe_tile"])
        img = clahe.apply(img)

    # Blur
    if params["blur"] == "median":
        k = params["median_ksize"]
        img = cv2.medianBlur(img, k)
    elif params["blur"] == "gaussian":
        ksize = params["gaussian_ksize"]
        sigma = params["gaussian_sigma"]
        if ksize is not None and sigma is not None:
            img = cv2.GaussianBlur(img, ksize, sigma)

    # Bilateral filter
    if params["bilateral"]:
        img = cv2.bilateralFilter(img,
                                  params["bilateral_diameter"],
                                  params["bilateral_sigma_color"],
                                  params["bilateral_sigma_space"])

    # Threshold + Invert
    img = apply_threshold(img, params["threshold"], params["invert"])

    # Sharpen
    if params["sharpen"]:
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        img = cv2.filter2D(img, -1, kernel)

    # Morphological operations
    kernel_size = params["morph_kernel"]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    if params["morph_open"] > 0:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=params["morph_iterations"])
    if params["morph_close"] > 0:
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=params["morph_iterations"])

    # Dilate
    if params["dilate"] > 0:
        dilate_kernel = np.ones((3, 3), np.uint8)
        img = cv2.dilate(img, dilate_kernel, iterations=params["dilate"])

    # Erode
    if params["erode"] > 0:
        erode_kernel = np.ones((3, 3), np.uint8)
        img = cv2.erode(img, erode_kernel, iterations=params["erode"])

    return img


def evaluate_ocr(img):
    """
    Avalia a imagem via pytesseract e retorna a média da confiança e tamanho do texto extraído.
    Usa pytesseract.image_to_data para pegar as confidências.
    """
    data = pytesseract.image_to_data(img, lang='por', output_type=pytesseract.Output.DICT)
    confidences = [int(conf) for conf in data['conf'] if conf.isdigit() and int(conf) >= 0]
    avg_conf = np.mean(confidences) if confidences else 0
    text = "".join(data['text']).strip()
    length = len(text)
    # Score combinado: média da confiança * tamanho texto (ponderação)
    score = avg_conf * length
    return score


def objective(trial, param_grid, pil_img):
    params = {}
    for key, values in param_grid.items():
        params[key] = trial.suggest_categorical(key, values)
    img_proc = preprocess_image(pil_img, params)
    score = evaluate_ocr(img_proc)
    # Minimizar o negativo do score para maximizar o score
    return -score


def optimize_pdf(pdf_path, param_grid, n_trials=30, n_jobs=1):
    images = pdf_to_images(pdf_path)
    results = []
    for i, pil_img in enumerate(images):
        logging.info(f"Otimizando página {i + 1}/{len(images)} do arquivo {os.path.basename(pdf_path)}")
        study = optuna.create_study(
            study_name=f"{os.path.basename(pdf_path)}_page_{i + 1}",
            direction="minimize",
            sampler=optuna.samplers.TPESampler(seed=42)
        )
        study.optimize(lambda trial: objective(trial, param_grid, pil_img), n_trials=n_trials, n_jobs=n_jobs)
        logging.info(f"Melhores parâmetros página {i + 1}: {study.best_params}")
        logging.info(f"Score: {-study.best_value}")
        results.append({
            "page": i + 1,
            "best_params": study.best_params,
            "best_score": -study.best_value,
        })
    return results


def run_folder(folder_path, param_grid, n_trials=30, n_jobs=1, save_json=True):
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    all_results = {}
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        logging.info(f"\nIniciando otimização do arquivo: {pdf_file}")
        results = optimize_pdf(pdf_path, param_grid, n_trials, n_jobs)
        all_results[pdf_file] = results
        if save_json:
            json_path = os.path.join(folder_path, f"{pdf_file}_opt_results.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            logging.info(f"Resultados salvos em {json_path}")
    return all_results


if __name__ == "__main__":
    folder_with_pdfs = r"/home/wallingson/Github/Account_bot-main/files/DCTF"
    # Exemplo: use n_jobs > 1 para paralelizar (depende do seu CPU)
    results = run_folder(folder_with_pdfs, param_grid_1, n_trials=30, n_jobs=2)