from PySide6.QtWidgets import QComboBox, QFormLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from estilos import ESTILO_GERAL
from base import BaseTela
from main import Contador
from contador_methods import ContadorMethods
from PySide6.QtCore import Qt

class TelaBoasVindas(BaseTela):
    def __init__(self, contador: Contador, usuario: str):
        super().__init__()
        self.contador = contador
        self.usuario = usuario
        self.setWindowTitle("Account Bot")
        self.setStyleSheet(ESTILO_GERAL)  # Aplica o estilo geral
        self.init_ui()

    def init_ui(self):
        # Logo e título
        self.adicionar_logo(120)
        self.adicionar_label("Account Bot", "titulo")
        self.adicionar_label(f"Olá, {self.usuario}!\nSeja bem-vindo!", "subtitulo")

        # Botões de conjuntos na mesma linha
        botoes = {
            "Ferramentas Gerais": "my_tools",
            "Importar DCOMP": "import_dcomp",
            "Tabulação de PDFs": "tabulates"
        }
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(15)  # Ajuste do espaçamento entre os botões
        for texto, tipo in botoes.items():
            btn = self.criar_botao(texto, "card", lambda checked, t=tipo: self.abrir_tela_inicial(t), largura=250, altura=60)
            layout_botoes.addWidget(btn)
        self.layout.addLayout(layout_botoes)

        # Botão sair centralizado abaixo
        btn_sair = self.criar_botao("Sair", "sair", self.close, largura=120, altura=50)
        self.layout.addWidget(btn_sair, alignment=Qt.AlignCenter)

        # Espaçador final
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def abrir_tela_inicial(self, conjunto: str):
        self.tela_inicial = TelaInicial(
            self.contador,
            conjunto,
            voltar_callback=lambda: TelaBoasVindas(self.contador, self.usuario).show()
        )
        self.tela_inicial.show()
        self.close()


class TelaInicial(BaseTela):
    def __init__(self, contador: Contador, conjunto="my_tools", voltar_callback=None):
        super().__init__()
        self.contador = contador
        self.conjunto = conjunto
        self.methods = ContadorMethods(contador)
        self.voltar_callback = voltar_callback
        self.setWindowTitle(f"Interface Contador - {self.conjunto}")
        self.setStyleSheet(ESTILO_GERAL)  # Aplica o estilo geral
        self.showFullScreen()  # Força a tela cheia apenas aqui
        self.init_ui()

    def init_ui(self):
        # Logo e instrução
        self.adicionar_logo(100)
        self.adicionar_label("Selecione a função:")

        # Combo de funções
        self.func_combo = QComboBox()
        self.func_combo.currentIndexChanged.connect(self.update_form)
        self.layout.addWidget(self.func_combo)

        # Formulário dinâmico
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        # Botões lado a lado
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(15)  # Ajuste de espaçamento entre os botões
        btn_executar = self.criar_botao("Executar", "card", self.execute_func, largura=200, altura=50)
        btn_voltar = self.criar_botao("Voltar", "voltar", self.voltar, largura=200, altura=50)
        layout_botoes.addWidget(btn_executar)
        layout_botoes.addWidget(btn_voltar)
        self.layout.addLayout(layout_botoes)

        # Inicializa funções
        self.methods.current_tool_set = self.conjunto
        self.methods.update_func_combo(self.func_combo)
        self.update_form()

        # Espaçador final
        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def update_form(self):
        func_display = self.func_combo.currentText()
        self.methods.mostrar_formulario(func_display, self.form_layout)

    def execute_func(self):
        func_display = self.func_combo.currentText()
        func_key = self.methods.get_func_key(func_display)
        try:
            resultado = f"Função selecionada: {func_key} (Conjunto: {self.conjunto})"
            QMessageBox.information(self, "Resultado", resultado)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def voltar(self):
        if self.voltar_callback:
            self.voltar_callback()
        self.close()
