# contador_methods.py
import os
import shutil
from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QComboBox, QMessageBox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ContadorMethods:
    def __init__(self, contador):
        self.contador = contador
        self.entries = {}
        self.current_tool_set = "my_tools"

        # --- Sets de funções ---
        self.my_tools = {
            "comparar_excel": "Conciliar planilhas",
            "consultar_cnpj": "Consulta CNPJ",
            "dividir_excel_por_item_de_coluna": "Dividir Excel por Item de Coluna",
            "dividir_pdf": "Dividir pdf por páginas",
            "limpar_pastas_de_arquivos_indesejados": "Limpar Pastas de Arquivos Indesejados",
            "mover_arquivos_xml_metade": "Mover Arquivos XML Metade",
            "organizar_XML_por_data": "Organizar XML por Data",
            "mover_arquivos_por_extensão": "Mover Arquivos por Extensão",
            "unificar_Excel_da_pasta": "Unificar Excel da Pasta"
        }

        self.import_dcomp = {
            "R11_R12": "Gerar arquivo R11/R12",
            "R13": "Gerar arquivo R13",
            "R15": "Gerar arquivo R15",
            "R21": "Gerar arquivo R21"
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

    # --- Download de arquivo ---
    def baixar_arquivo(self, arquivo_selecionado, parent=None):
        pasta_destino = QFileDialog.getExistingDirectory(parent, "Escolher pasta para salvar")
        if pasta_destino:
            try:
                shutil.copy(os.path.join(BASE_DIR, "static", arquivo_selecionado), pasta_destino)
                QMessageBox.information(parent, "Download", f"{arquivo_selecionado} baixado com sucesso!")
            except Exception as e:
                QMessageBox.critical(parent, "Erro", f"Falha ao baixar o arquivo: {e}")

    # --- Alternar conjuntos de funções ---
    def switch_function_set(self):
        if self.current_tool_set == "my_tools":
            self.current_tool_set = "tabulates"
        elif self.current_tool_set == "tabulates":
            self.current_tool_set = "import_dcomp"
        else:
            self.current_tool_set = "my_tools"

    # --- Atualizar combo de funções ---
    def update_func_combo(self, combo):
        combo.clear()
        if self.current_tool_set == "my_tools":
            combo.addItems(self.my_tools.values())
        elif self.current_tool_set == "tabulates":
            combo.addItems(self.tabulates.values())
        elif self.current_tool_set == "import_dcomp":
            combo.addItems(self.import_dcomp.values())

    # --- Obter chave pelo display ---
    def get_func_key(self, display_text):
        if self.current_tool_set == "my_tools":
            for k, v in self.my_tools.items():
                if v == display_text:
                    return k
        elif self.current_tool_set == "tabulates":
            for k, v in self.tabulates.items():
                if v == display_text:
                    return k
        elif self.current_tool_set == "import_dcomp":
            for k, v in self.import_dcomp.items():
                if v == display_text:
                    return k
        return None

    # --- Mostrar formulário dinâmico ---
    def mostrar_formulario(self, func_display, form_layout):
        # Limpar form antigo
        for i in reversed(range(form_layout.count())):
            item = form_layout.itemAt(i)
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
                form_layout.addRow(nome + ":", container)
                self.entries[nome] = campo
            else:
                campo = QLineEdit()
                if placeholder:
                    campo.setPlaceholderText(placeholder)
                form_layout.addRow(nome + ":", campo)
                self.entries[nome] = campo

        # --- Formulários por set ---
        if self.current_tool_set == "my_tools":
            if func == "comparar_excel":
                criar_entry("caminho_excel_origem", "file")
                criar_entry("aba_origem")
                criar_entry("linhas_pular_origem", placeholder="Número inteiro, ex: 0")
                criar_entry("caminho_excel_destino", "file")
                criar_entry("aba_destino")
                criar_entry("linhas_pular_destino", placeholder="Número inteiro, ex: 0")
                criar_entry("colunas_chave_origem", placeholder="Ex: CNPJ,Nome,Data")
                criar_entry("colunas_chave_destino", placeholder="Ex: CNPJ,Nome,Data")
                criar_entry("diretorio_saida", "folder")
            elif func == "consultar_cnpj":
                criar_entry("Taxa de consulta (por minuto)", placeholder="3")
                criar_entry("Arquivo Excel de entrada", "file")
                criar_entry("Arquivo Excel de saída", placeholder="resultado_cnpjs.xlsx")
            elif func == "dividir_excel_por_item_de_coluna":
                criar_entry("Arquivo Excel", "file")
                criar_entry("Coluna de divisão")
                criar_entry("Diretório de saída", "folder")
            elif func == "dividir_pdf":
                criar_entry("PDF de entrada", "file")
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
                form_layout.addRow("Organizar por:", cb)
                self.entries["Organizar por"] = cb
            elif func == "mover_arquivos_por_extensão":
                criar_entry("Diretório raiz", "folder")
                criar_entry("Pasta output", "folder")
                criar_entry("Extensão desejada (ex: .xml)")
            elif func == "unificar_Excel_da_pasta":
                criar_entry("Pasta", "folder")

        elif self.current_tool_set == "import_dcomp":
            if func in self.import_dcomp:
                criar_entry("Arquivo Excel de entrada", "file")
                criar_entry("Diretório de saída", "folder")

        else:  # tabulates
            criar_entry("Pasta com PDFs", "folder")
            cb_ocr = QComboBox()
            cb_ocr.addItems(["Sim", "Não"])
            form_layout.addRow("Usar OCR?", cb_ocr)
            self.entries["Usar OCR"] = cb_ocr

    # --- Seleção ---
    def selecionar_arquivo(self, campo):
        arquivo, _ = QFileDialog.getOpenFileName(None, "Selecionar arquivo")
        if arquivo:
            campo.setText(arquivo)

    def selecionar_pasta(self, campo):
        pasta = QFileDialog.getExistingDirectory(None, "Selecionar pasta")
        if pasta:
            campo.setText(pasta)
