# telas/utils.py
import os
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

# Diretório base
import sys
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def centralizar_widget(widget):
    qr = widget.frameGeometry()
    cp = widget.screen().availableGeometry().center()
    qr.moveCenter(cp)
    widget.move(qr.topLeft())

def criar_logo(tamanho=120):
    caminho = os.path.abspath(os.path.join(BASE_DIR, "..", "assets", "D2X.png"))
    lbl = QLabel()
    pix = QPixmap(caminho).scaled(tamanho, tamanho, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    lbl.setPixmap(pix)
    lbl.setAlignment(Qt.AlignCenter)
    return lbl

def criar_botao(texto, nome, callback):
    btn = QPushButton(texto)
    btn.setObjectName(nome)
    btn.clicked.connect(callback)
    return btn
