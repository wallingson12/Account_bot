import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QWidget,
    QComboBox, QFormLayout, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from main import Contador  # sua classe original
from account_tools.api import autenticar_api  # sua função de autenticação
from config.config import caminho_tesseract

# --- Dialog de Login ---
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
# ...

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(600, 600)

        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e3f2fd, stop:1 #bbdefb);
                }
            QLabel {
               font-weight: bold;
               qproperty-alignment: 'AlignCenter';
               }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QPushButton#cancelar {
                background-color: #aaa;
            }
            QPushButton#cancelar:hover {
                background-color: #888;
            }
            QPushButton#cadastrar {
                background-color: #4caf50;
            }
            QPushButton#cadastrar:hover {
                background-color: #388e3c;
            }
        """)

        self.usuario = None
        self.senha = None

        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)
        layout_form = QFormLayout()
        layout_form.setSpacing(10)

        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Digite seu usuário")

        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password)
        self.senha_input.setPlaceholderText("Digite sua senha")

        layout_form.addRow("Usuário:", self.usuario_input)
        layout_form.addRow("Senha:", self.senha_input)

        btns = QHBoxLayout()
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

# --- Interface Principal ---
class ContadorGUI(QWidget):
    def __init__(self, contador):
        super().__init__()
        self.contador = contador
        self.entries = {}

        self.setWindowTitle("Interface Contador")
        self.setFixedSize(600, 500)

        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()

        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #e3f2fd, stop:1 #bbdefb);
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QLabel {
                background-color: transparent;
                font-weight: bold;
            }

            QComboBox, QLineEdit, QTextEdit {
                border: 1px solid #aaa;
                border-radius: 6px;
                padding: 6px;
            }

            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #005fa3;
            }

            QTextEdit {
                background-color: #1e1e1e;
                color: #dcdcdc;
                border: 1px solid #444;
                font-family: Consolas, monospace;
            }
        """)

        layout = QVBoxLayout()

        btn_sobre = QPushButton("Sobre")

        # Função normal dentro do __init__, sem self
        def abrir_sobre():
            QDesktopServices.openUrl(QUrl("http://127.0.0.1:8000/home"))

        btn_sobre.clicked.connect(abrir_sobre)
        layout.addWidget(btn_sobre, alignment=Qt.AlignRight)

        pix = QPixmap(r"assets\D2X.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label = QLabel()
        icon_label.setPixmap(pix)
        icon_label.setFixedSize(64, 64)
        icon_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        top_box = QVBoxLayout()
        top_box.setAlignment(Qt.AlignCenter)
        top_box.addWidget(icon_label)
        layout.addLayout(top_box)

        self.my_tools = {
            "processar_e_classificar_unificado": "Processar e Classificar Unificado",
            "consulta_cnpj": "Consulta CNPJ",
            "dividir_excel_por_item_de_coluna": "Dividir Excel por Item de Coluna",
            "dividir_pdf": "Dividir pdf por páginas",
            "limpar_pastas_de_arquivos_indesejados": "Limpar Pastas de Arquivos Indesejados",
            "mover_arquivos_xml_metade": "Mover Arquivos XML Metade",
            "organizar_XML_por_data": "Organizar XML por Data",
            "mover_arquivos_por_extensão": "Mover Arquivos por Extensão",
            "unificar_Excel_da_pasta": "Unificar Excel da Pasta"
        }

        self.import_dcomp = {
            "R11/R12":"Gerar arquivo R11/R12"
        }

        self.tabulates = {
            "processar_pdfs_dctf": "Tabular DCTF",
            "processar_fontes_pagadoras": "Tabular Fontes Pagadoras",
            "processar_darf_pdfs": "Tabular DARF",
            "processar_pdfs_ocr_free": "Tabular Free",
            "processar_cfop_pdfs": "Tabular CFOP",
            "processar_dcomp_pdfs": "Tabular DCOMP",
            "processar_recolhimentos_pdfs": "Tabular Extrato de Recolhimentos"
        }

        self.current_tool_set = "my_tools"

        self.switch_button = QPushButton("Switch to Tabulates")
        self.switch_button.clicked.connect(self.switch_function_set)
        layout.addWidget(self.switch_button)

        label = QLabel("Selecione a função:")
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(label)

        self.func_combo = QComboBox()
        layout.addWidget(self.func_combo)
        self.func_combo.currentIndexChanged.connect(self.mostrar_formulario)

        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)

        self.exec_button = QPushButton("Executar")
        self.exec_button.clicked.connect(self.execute_my_tools)
        layout.addWidget(self.exec_button)

        self.setLayout(layout)
        self.update_func_combo()

    def switch_function_set(self):
        if self.current_tool_set == "my_tools":
            self.current_tool_set = "tabulates"
            self.switch_button.setText("Switch to Import DCOMP")
        elif self.current_tool_set == "tabulates":
            self.current_tool_set = "import_dcomp"
            self.switch_button.setText("Switch to My Tools")
        else:
            self.current_tool_set = "my_tools"
            self.switch_button.setText("Switch to Tabulates")
        self.update_func_combo()

    def update_func_combo(self):
        self.func_combo.clear()
        if self.current_tool_set == "my_tools":
            # junta as funções do My Tools com as do Import DCOMP
            todas_funcoes = list(self.my_tools.values()) + list(self.import_dcomp.values())
            self.func_combo.addItems(todas_funcoes)
        elif self.current_tool_set == "tabulates":
            self.func_combo.addItems(self.tabulates.values())
        elif self.current_tool_set == "import_dcomp":
            self.func_combo.addItems(self.import_dcomp.values())
        self.mostrar_formulario()

    def get_func_key(self, display_text):
        if self.current_tool_set == "my_tools":
            dict_combined = {**self.my_tools, **self.import_dcomp}
            for key, val in dict_combined.items():
                if val == display_text:
                    return key
        elif self.current_tool_set == "tabulates":
            for key, val in self.tabulates.items():
                if val == display_text:
                    return key
        elif self.current_tool_set == "import_dcomp":
            for key, val in self.import_dcomp.items():
                if val == display_text:
                    return key
        return None

    def mostrar_formulario(self):
        # Limpar form antigo
        for i in reversed(range(self.form_layout.count())):
            item = self.form_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                layout = item.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                layout.deleteLater()
        self.entries.clear()

        func_display = self.func_combo.currentText()
        func = self.get_func_key(func_display)

        def criar_entry(nome, tipo="text", placeholder=None):
            if tipo in ("folder", "file"):
                campo = QLineEdit()
                btn = QPushButton("Selecionar")
                if tipo == "folder":
                    btn.clicked.connect(lambda: self.selecionar_pasta(campo))
                else:
                    btn.clicked.connect(lambda: self.selecionar_arquivo(campo))
                container = QHBoxLayout()
                container.addWidget(campo)
                container.addWidget(btn)
                self.form_layout.addRow(nome + ":", container)
                self.entries[nome] = campo
            else:
                campo = QLineEdit()
                if placeholder:
                    campo.setPlaceholderText(placeholder)
                self.form_layout.addRow(nome + ":", campo)
                self.entries[nome] = campo

        if self.current_tool_set == "my_tools":
            if func == "processar_e_classificar_unificado":
                criar_entry("Arquivo Excel 1", "file")
                criar_entry("Nome da aba 1")
                criar_entry("Linhas a pular 1", placeholder="Número inteiro, ex: 0")
                criar_entry("Arquivo Excel 2", "file")
                criar_entry("Nome da aba 2")
                criar_entry("Linhas a pular 2", placeholder="Número inteiro, ex: 0")
                criar_entry("Colunas do Excel 1 (separadas por vírgula)", placeholder="Ex: CNPJ,Nome,Data")
                criar_entry("Colunas do Excel 2 (separadas por vírgula)", placeholder="Ex: CNPJ,Nome,Data")
                criar_entry("Diretório de saída", "folder")

            elif func == "consulta_cnpj":
                criar_entry("Taxa de consulta (por minuto)", placeholder="3")
                criar_entry("Arquivo Excel de entrada", "file")
                criar_entry("Arquivo Excel de saída", placeholder="resultado_cnpjs.xlsx")

            elif func == "dividir_excel_por_item_de_coluna":
                criar_entry("Arquivo Excel", "file")
                criar_entry("Coluna de divisão")
                criar_entry("Diretório de saída", "folder")

            elif func == "limpar_pastas_de_arquivos_indesejados":
                criar_entry("Pasta raiz", "folder")
                criar_entry("Formato para manter (ex: .xlsx)")

            elif func == "mover_arquivos_xml_metade":
                criar_entry("Diretório origem", "folder")
                criar_entry("Diretório destino", "folder")

            elif func == "organizar_XML_por_data":
                criar_entry("Diretório origem", "folder")
                criar_entry("Diretório destino", "folder")
                cb = QComboBox()
                cb.addItems(["ano", "mes/ano"])
                self.form_layout.addRow("Organizar por:", cb)
                self.entries["Organizar por"] = cb

            elif func == "mover_arquivos_por_extensão":
                criar_entry("Diretório raiz", "folder")
                criar_entry("Pasta output", "folder")
                criar_entry("Extensão desejada (ex: .xml)")

            elif func == "unificar_Excel_da_pasta":
                criar_entry("Pasta", "folder")

            elif func in self.import_dcomp:
                # ex: R11/R12
                criar_entry("Pasta de entrada", "folder")
                criar_entry("Arquivo de saída")

        elif self.current_tool_set == "import_dcomp":
            if func == "R11/R12":
                criar_entry("Pasta de entrada", "folder")
                criar_entry("Arquivo de saída")

        else:  # tabulates
            # Todas as funções de tabulates têm assinatura (pasta_pdfs, usar_ocr=True/False)
            criar_entry("Pasta com PDFs", "folder")
            cb_ocr = QComboBox()
            cb_ocr.addItems(["Sim", "Não"])
            self.form_layout.addRow("Usar OCR?", cb_ocr)
            self.entries["Usar OCR"] = cb_ocr

    def selecionar_arquivo(self, campo):
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo")
        if arquivo:
            campo.setText(arquivo)

    def selecionar_pasta(self, campo):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        if pasta:
            campo.setText(pasta)

    def execute_my_tools(self):
        func_display = self.func_combo.currentText()
        func = self.get_func_key(func_display)

        try:
            resultado = None

            if self.current_tool_set == "my_tools":
                if func == "processar_e_classificar_unificado":
                    path1 = self.entries["Arquivo Excel 1"].text()
                    aba1 = self.entries["Nome da aba 1"].text()
                    pular1 = int(self.entries["Linhas a pular 1"].text())
                    path2 = self.entries["Arquivo Excel 2"].text()
                    aba2 = self.entries["Nome da aba 2"].text()
                    pular2 = int(self.entries["Linhas a pular 2"].text())
                    cols1 = [c.strip() for c in self.entries["Colunas do Excel 1 (separadas por vírgula)"].text().split(",")]
                    cols2 = [c.strip() for c in self.entries["Colunas do Excel 2 (separadas por vírgula)"].text().split(",")]
                    dir_saida = self.entries["Diretório de saída"].text()

                    resultado = self.contador.processar_e_classificar_unificado(
                        path1, aba1, pular1, path2, aba2, pular2, cols1, cols2, dir_saida
                    )

                elif func == "consulta_cnpj":
                    taxa = self.entries["Taxa de consulta (por minuto)"].text()
                    entrada = self.entries["Arquivo Excel de entrada"].text()
                    saida = self.entries["Arquivo Excel de saída"].text()

                    resultado = self.contador.consulta_cnpj(
                        taxa_consulta=int(taxa) if taxa else 3,
                        arquivo_entrada=entrada,
                        arquivo_saida=saida
                    )

                elif func == "dividir_excel_por_item_de_coluna":
                    resultado = self.contador.dividir_excel(
                        arquivo_excel=self.entries["Arquivo Excel"].text(),
                        coluna_divisao=self.entries["Coluna de divisão"].text(),
                        diretorio_output=self.entries["Diretório de saída"].text()
                    )

                elif func == "limpar_pastas_de_arquivos_indesejados":
                    resultado = self.contador.limpar_arquivos_por_formato(
                        pasta_raiz=self.entries["Pasta raiz"].text(),
                        formato_manter=self.entries["Formato para manter (ex: .xlsx)"].text()
                    )

                elif func == "mover_arquivos_xml_metade":
                    resultado = self.contador.mover_arquivos_esocial(
                        self.entries["Diretório origem"].text(),
                        self.entries["Diretório destino"].text()
                    )

                elif func == "organizar_XML_por_data":
                    dir_origem = self.entries["Diretório origem"].text()
                    organizar_por = self.entries["Organizar por"].currentText()
                    resultado = self.contador.organizar_xml_por_data(dir_origem, organizar_por)

                elif func == "mover_arquivos_por_extensão":
                    resultado = self.contador.mover_arquivos_por_extensao(
                        self.entries["Diretório raiz"].text(),
                        self.entries["Pasta output"].text(),
                        self.entries["Extensão desejada (ex: .xml)"].text()
                    )

                elif func == "unificar_Excel_da_pasta":
                    resultado = self.contador.unificar_excel_da_pasta(
                        self.entries["Pasta"].text()
                    )
                else:
                    resultado = "Função não implementada."

            elif self.current_tool_set == "import_dcomp":
                if func == "R11/R12":
                    entrada = self.entries["Pasta de entrada"].text()
                    saida = self.entries["Arquivo de saída"].text()
                    resultado = self.contador.gerar_r11_r12(entrada, saida)
                else:
                    resultado = "Função não implementada."

            elif self.current_tool_set == "tabulates":
                pasta = self.entries["Pasta com PDFs"].text()
                usar_ocr = self.entries["Usar OCR"].currentText() == "Sim"

                if hasattr(self.contador, func):
                    funcao = getattr(self.contador, func)
                    resultado = funcao(pasta, usar_ocr)
                else:
                    resultado = "Função não implementada."

            if resultado is None:
                resultado = "(sem mensagem de retorno)"

            QMessageBox.information(self, "Resultado", str(resultado))

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))


# --- Função de autenticação ---
def autenticar_usuario_gui():
    for _ in range(3):
        login_dialog = LoginDialog()
        result = login_dialog.exec()

        if result != QDialog.Accepted:
            return None

        try:
            resposta = autenticar_api(login_dialog.usuario, login_dialog.senha)
            return resposta
        except Exception as e:
            QMessageBox.warning(None, "Erro", f"Falha na autenticação: {e}")

    return None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    usuario_logado = autenticar_usuario_gui()
    if usuario_logado is None:
        QMessageBox.warning(None, "Login", "Falha na autenticação. Encerrando.")
        sys.exit()

    contador = Contador(caminho_tesseract)
    janela = ContadorGUI(contador)
    janela.show()

    sys.exit(app.exec())
