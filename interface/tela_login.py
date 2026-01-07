import sys
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDialog, QApplication, QFormLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QLabel

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Account Bot")
        self.setFixedSize(600, 600)

        # Centralizar
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Estilo tipo Twitter
        self.setStyleSheet("""
            QDialog {
                background-color: #E6F0FA;  /* fundo azul clarinho */
                font-family: 'Segoe UI', sans-serif;
                color: #14171A;
            }
            QLabel {
                background: transparent;
                border: none;
                color: #14171A;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #AAB8C2;
                border-radius: 12px;
                font-size: 20px;  /* tamanho do texto igual ao botão */
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #1DA1F2;  /* azul Twitter */
                color: #FFFFFF;
                border-radius: 20px;
                padding: 10px 24px;
                font-size: 20px;  /* mesmo tamanho do label */
                font-weight: 800;
            }
            QPushButton:hover {
                background-color: #0d95e8;
            }
            QPushButton#cancelar {
                background-color: #E0245E;  /* vermelho Twitter */
            }
            QPushButton#cancelar:hover {
                background-color: #c81e51;
            }
            QPushButton#cadastrar {
                background-color: #4CAF50;  /* verde */
            }
            QPushButton#cadastrar:hover {
                background-color: #388e3c;
            }
        """)

        self.usuario = None
        self.senha = None

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)
        layout_principal.setSpacing(25)

        # --- TÍTULO GRANDE ---
        titulo_label = QLabel("Account Bot")
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("font-size: 36px; font-weight: 900; color: #14171A;")
        layout_principal.addWidget(titulo_label)

        # Formulário
        layout_form = QFormLayout()
        layout_form.setSpacing(15)

        # Inputs
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Digite seu usuário")

        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password)
        self.senha_input.setPlaceholderText("Digite sua senha")

        # Labels do mesmo tamanho dos botões
        lbl_usuario = QLabel("Usuário:")
        lbl_usuario.setStyleSheet("font-size: 20px; font-weight: 800; color: #14171A;")
        lbl_senha = QLabel("Senha:")
        lbl_senha.setStyleSheet("font-size: 20px; font-weight: 800; color: #14171A;")

        layout_form.addRow(lbl_usuario, self.usuario_input)
        layout_form.addRow(lbl_senha, self.senha_input)

        # Botões
        btns = QHBoxLayout()
        btns.setSpacing(15)
        btns.setAlignment(Qt.AlignCenter)

        btn_ok = QPushButton("Entrar")
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("cancelar")
        btn_cadastrar = QPushButton("Cadastrar")
        btn_cadastrar.setObjectName("cadastrar")

        btn_ok.clicked.connect(self.accept_login)
        btn_cancel.clicked.connect(self.reject)
        btn_cadastrar.clicked.connect(self.abrir_cadastro)

        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_cadastrar)

        # Adiciona tudo ao layout principal
        layout_principal.addLayout(layout_form)
        layout_principal.addLayout(btns)
        self.setLayout(layout_principal)

    def accept_login(self):
        self.usuario = self.usuario_input.text()
        self.senha = self.senha_input.text()
        if not self.usuario or not self.senha:
            QMessageBox.warning(self, "Aviso", "Preencha usuário e senha.")
            return
        self.accept()

    def abrir_cadastro(self):
        QDesktopServices.openUrl(QUrl("http://localhost:8000/auth/cadastrar/"))


# --- Teste rápido ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = LoginDialog()
    dlg.exec()
