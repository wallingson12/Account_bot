import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from main import Contador

class TestContadorIntegracao(unittest.TestCase):
    def setUp(self):
        # Cria o objeto Contador
        self.contador = Contador()
        # Cria pastas temporárias
        self.temp_dir = tempfile.TemporaryDirectory()
        self.pasta_base = Path(self.temp_dir.name)

        # Cria arquivos simulados
        self.excel1 = self.pasta_base / "file1.xlsx"
        self.excel2 = self.pasta_base / "file2.xlsx"
        self.xml_file = self.pasta_base / "arquivo.xml"
        self.pdf_file = self.pasta_base / "arquivo.pdf"

        self.excel1.touch()
        self.excel2.touch()
        self.xml_file.touch()
        self.pdf_file.touch()

    def tearDown(self):
        # Limpa pastas temporárias
        self.temp_dir.cleanup()

    # ===== EXCEL =====
    def test_dividir_unificar_excel(self):
        # Testa dividir e unificar (simulação)
        with patch.object(self.contador, 'dividir_excel', return_value="Dividido"):
            resultado = self.contador.dividir_excel(str(self.excel1), "Coluna", str(self.pasta_base))
            self.assertEqual(resultado, "Dividido")

        with patch.object(self.contador, 'unificar_excel', return_value="Unificado"):
            resultado = self.contador.unificar_excel(str(self.pasta_base))
            self.assertEqual(resultado, "Unificado")

    def test_comparar_excel(self):
        with patch.object(self.contador, 'comparar_excel', return_value="Comparado"):
            resultado = self.contador.comparar_excel(
                str(self.excel1), "Sheet1", 0,
                str(self.excel2), "Sheet2", 0,
                ["CNPJ"], ["CNPJ"], str(self.pasta_base)
            )
            self.assertEqual(resultado, "Comparado")

    # ===== FILES =====
    def test_limpar_mover_pastas(self):
        with patch.object(self.contador, 'limpar_pasta', return_value="Pasta limpa"):
            resultado = self.contador.limpar_pasta(str(self.pasta_base), ".xlsx")
            self.assertEqual(resultado, "Pasta limpa")

        with patch.object(self.contador, 'mover_extensao', return_value="Arquivos movidos"):
            resultado = self.contador.mover_extensao(str(self.pasta_base), str(self.pasta_base), ".xml")
            self.assertEqual(resultado, "Arquivos movidos")

    # ===== XML =====
    def test_mover_organizar_xml(self):
        with patch.object(self.contador, 'mover_esocial', return_value="Esocial movido"):
            resultado = self.contador.mover_esocial(str(self.pasta_base), str(self.pasta_base))
            self.assertEqual(resultado, "Esocial movido")

        with patch.object(self.contador, 'organizar_xml', return_value="XML organizado"):
            resultado = self.contador.organizar_xml(str(self.pasta_base), str(self.pasta_base), "ano")
            self.assertEqual(resultado, "XML organizado")

    # ===== CNPJ =====
    def test_consultar_cnpj(self):
        with patch.object(self.contador, 'consultar_cnpj', return_value="CNPJs consultados"):
            resultado = self.contador.consultar_cnpj(taxa_consulta=3, arquivo_entrada=str(self.excel1), arquivo_saida=str(self.excel2))
            self.assertEqual(resultado, "CNPJs consultados")

    # ===== PDF =====
    def test_dividir_pdf(self):
        with patch.object(self.contador, 'dividir_pdf', return_value="PDF dividido"):
            resultado = self.contador.dividir_pdf(str(self.pdf_file))
            self.assertEqual(resultado, "PDF dividido")

    # ===== TABULADORES =====
    def test_tabuladores(self):
        tab_funcs = ['dctf', 'darf', 'fontes', 'cfop', 'dcomp', 'dcomp_ipi', 'recolhimentos', 'ocr_livre']
        for func_name in tab_funcs:
            with patch.object(self.contador, func_name, return_value=f"{func_name.upper()} processado"):
                func = getattr(self.contador, func_name)
                resultado = func(str(self.pasta_base))
                self.assertEqual(resultado, f"{func_name.upper()} processado")

    # ===== IPI =====
    def test_ipi(self):
        ipi_funcs = ['r11_r12', 'r13', 'r15', 'r21']
        for func_name in ipi_funcs:
            with patch.object(self.contador, func_name, return_value=f"{func_name.upper()} gerado"):
                func = getattr(self.contador, func_name)
                resultado = func(str(self.excel1), str(self.pasta_base))
                self.assertEqual(resultado, f"{func_name.upper()} gerado")


if __name__ == "__main__":
    unittest.main()
