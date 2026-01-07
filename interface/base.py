from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os
import sys

# Diretório base
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BaseTela(QWidget):
    def __init__(self, largura=800, altura=800):
        super().__init__()

        self.layout = QVBoxLayout()  # Layout principal para a tela
        self.setLayout(self.layout)
        self.centralizar()

        # Ajustando espaçamento para 10 (diminuindo o espaçamento entre os elementos)
        self.layout.setSpacing(10)

        # **Logo**: Criando um layout fixo para a logo (isso impede que a logo afete outros elementos)
        self.logo_layout = QVBoxLayout()  # Layout exclusivo para logo
        self.layout.addLayout(self.logo_layout)

        # **Espaçador entre logo e título**: Garante que o título e outros elementos fiquem abaixo de forma estável
        self.layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

    def ajustar_tamanho_automatico(self):
        """
        Ajusta o tamanho da janela com base no conteúdo.
        """
        self.adjustSize()

    def centralizar(self):
        """
        Centraliza a janela na tela.
        """
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def adicionar_logo(self, tamanho=120):
        """
        Adiciona uma imagem de logo na tela.
        """
        caminho = os.path.abspath(os.path.join(BASE_DIR, "..", "assets", "D2X.png"))
        lbl = QLabel()
        pix = QPixmap(caminho).scaled(
            tamanho, tamanho,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        lbl.setPixmap(pix)
        lbl.setAlignment(Qt.AlignCenter)

        # Adicionando a logo no layout exclusivo da logo
        self.logo_layout.addWidget(lbl)

    def criar_botao(self, texto, nome, callback, largura=200, altura=50):
        """
        Cria um botão na tela.
        """
        btn = QPushButton(texto)
        btn.setObjectName(nome)
        btn.clicked.connect(callback)
        btn.setFixedSize(largura, altura)
        btn.setContentsMargins(5, 5, 5, 5)  # Ajustando margens menores
        self.layout.addWidget(btn, alignment=Qt.AlignCenter)
        return btn

    def adicionar_label(self, texto, nome=None, alinhamento=Qt.AlignCenter):
        """
        Adiciona um rótulo (label) na tela.
        """
        lbl = QLabel(texto)
        if nome:
            lbl.setObjectName(nome)
        lbl.setAlignment(alinhamento)
        self.layout.addWidget(lbl)
        return lbl
