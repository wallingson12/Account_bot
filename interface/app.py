# run_app.py
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QDialog
from tela_login import LoginDialog
from telas_principais import TelaBoasVindas  # Tela refatorada
from main import Contador
from account_tools.api import autenticar_api

def main():
    app = QApplication(sys.argv)

    # --- Tela de login ---
    login = LoginDialog()
    if login.exec() != QDialog.Accepted:
        sys.exit()  # Sai se o usuário cancelar o login

    usuario = login.usuario
    senha = login.senha

    try:
        # --- Autenticação via API ---
        token = autenticar_api(usuario, senha)
        if not token:
            QMessageBox.critical(None, "Erro", "Falha na autenticação. Verifique usuário e senha.")
            sys.exit()

        # --- Inicializa o contador ---
        contador = Contador()

        # --- Abre a tela de boas-vindas ---
        boas_vindas = TelaBoasVindas(contador, usuario)
        boas_vindas.show()

        sys.exit(app.exec())

    except Exception as e:
        QMessageBox.critical(None, "Erro inesperado", str(e))
        sys.exit()


if __name__ == "__main__":
    main()
