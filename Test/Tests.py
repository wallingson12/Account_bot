import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import tempfile

MODULE = "main"  # ajuste conforme o nome do arquivo que tem a classe Contador
from main import Contador


@pytest.fixture
def contador():
    return Contador(caminho_tesseract="/usr/bin/tesseract")


# Testes para métodos que apenas delegam para funções externas, mockando-as
@patch(f"{MODULE}.comparar_e_classificar_excel")
def test_processar_e_classificar_unificado(mock_comp, contador):
    mock_comp.return_value = pd.DataFrame({"A": [1, 2]})
    result = contador.processar_e_classificar_unificado("p1", "a1", 0, "p2", "a2", 1, ["c1"], ["c2"], "dir")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


@patch(f"{MODULE}.consulta_cnpj")
def test_consulta_cnpj(mock_consulta, contador):
    mock_consulta.return_value = {"cnpj": "00000000000191"}
    result = contador.consulta_cnpj()
    assert isinstance(result, dict)


@patch(f"{MODULE}.dividir_planilha_por_coluna")
def test_dividir_excel(mock_dividir, contador):
    mock_dividir.return_value = None
    result = contador.dividir_excel("arquivo.xlsx", "Coluna", "saida")
    assert result is None


@patch(f"{MODULE}.limpar_arquivos_por_formato")
def test_limpar_arquivos_por_formato(mock_limpar, contador):
    mock_limpar.return_value = None
    result = contador.limpar_arquivos_por_formato("pasta", ".xml")
    assert result is None


@patch(f"{MODULE}.mover_arquivos_xml_metade")
def test_mover_arquivos_esocial(mock_mover, contador):
    mock_mover.return_value = None
    result = contador.mover_arquivos_esocial("pasta_base", "pasta_dest", dividir=True)
    assert result is None


@patch(f"{MODULE}.organizar_xml_por_data")
def test_organizar_xml_por_data(mock_organizar, contador):
    mock_organizar.return_value = None
    result = contador.organizar_xml_por_data("pasta", organizar_por="ano")
    assert result is None


@patch(f"{MODULE}.mover_arquivos_por_extensao")
def test_mover_arquivos_por_extensao(mock_mover, contador):
    mock_mover.return_value = {"xml": 5}
    result = contador.mover_arquivos_por_extensao("raiz", "output", ".xml")
    assert isinstance(result, dict)
    assert "xml" in result


@patch(f"{MODULE}.unificar_excel_da_pasta")
def test_unificar_excel_da_pasta(mock_unificar, contador):
    mock_unificar.return_value = "pasta/arquivo_unificado.xlsx"
    result = contador.unificar_excel_da_pasta("pasta")
    assert isinstance(result, str)


@patch(f"{MODULE}.dividir_pdf")
def test_dividir_pdf(mock_dividir, contador):
    mock_dividir.return_value = ["p1.pdf", "p2.pdf"]
    result = contador.dividir_pdf("arquivo.pdf")
    assert isinstance(result, list)
    assert len(result) == 2


# Testar método processar_pdfs_dctf
@patch(f"{MODULE}.extrair_dctf_pdf")
@patch("os.listdir")
@patch("pandas.DataFrame.to_excel")
def test_processar_pdfs_dctf(mock_to_excel, mock_listdir, mock_extrair, contador, tmp_path):
    mock_listdir.return_value = ["a.pdf", "b.PDF", "outro.txt"]
    mock_extrair.side_effect = [
        (pd.DataFrame({"col": [1]}), None),
        (pd.DataFrame({"col": [2]}), None),
    ]
    resultado = contador.processar_pdfs_dctf(str(tmp_path))
    assert isinstance(resultado, pd.DataFrame)
    assert not resultado.empty


# Testar processar_pdfs_dctf com nenhum PDF
@patch("os.listdir")
def test_processar_pdfs_dctf_sem_pdfs(mock_listdir, contador, tmp_path):
    mock_listdir.return_value = ["arquivo.txt"]
    df = contador.processar_pdfs_dctf(str(tmp_path))
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# Testar processar_fontes_pagadoras com OCR desativado
def test_processar_fontes_pagadoras_ocr_desativado(contador, tmp_path):
    df = contador.processar_fontes_pagadoras(str(tmp_path), usar_ocr=False)
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# Testar processar_fontes_pagadoras com mocks e OCR ativado
@patch("os.listdir")
@patch(f"{MODULE}.pdf_to_images")
@patch(f"{MODULE}.extract_ocr_data_from_image")
@patch(f"{MODULE}.find_full_patterns")
@patch("pandas.DataFrame.to_excel")
def test_processar_fontes_pagadoras_ocr_ativo(mock_to_excel, mock_find, mock_extract, mock_pdf_to_img, mock_listdir, contador, tmp_path):
    mock_listdir.return_value = ["f1.pdf"]
    mock_pdf_to_img.return_value = ["img1"]
    mock_extract.return_value = ("texto extraido", None)
    mock_find.return_value = [
        ["123", "Nome", "01/01/2020", "001", 100, 10]
    ]
    df = contador.processar_fontes_pagadoras(str(tmp_path), usar_ocr=True)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# Testar processar_darf_pdfs com OCR desativado
def test_processar_darf_pdfs_ocr_desativado(contador, tmp_path):
    df = contador.processar_darf_pdfs(str(tmp_path), usar_ocr=False)
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# Testar processar_darf_pdfs com mocks e OCR ativo
@patch("os.listdir")
@patch(f"{MODULE}.pdf_to_images")
@patch(f"{MODULE}.extract_ocr_data_from_image")
@patch(f"{MODULE}.extrair_infos_darf")
@patch("pandas.DataFrame.to_excel")
def test_processar_darf_pdfs_ocr_ativo(mock_to_excel, mock_extrair_infos, mock_extract, mock_pdf_to_img, mock_listdir, contador, tmp_path):
    mock_listdir.return_value = ["a.pdf"]
    mock_pdf_to_img.return_value = ["img1", "img2"]
    mock_extract.return_value = ("texto", 90)
    mock_extrair_infos.return_value = [{"campo": 1}]
    df = contador.processar_darf_pdfs(str(tmp_path), usar_ocr=True)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# Testar processar_pdfs_ocr_free com OCR desativado
def test_processar_pdfs_ocr_free_ocr_desativado(contador, tmp_path):
    df = contador.processar_pdfs_ocr_free(str(tmp_path), usar_ocr=False)
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# Testar processar_pdfs_ocr_free com OCR ativo
@patch("os.listdir")
@patch(f"{MODULE}.pdf_to_images")
@patch(f"{MODULE}.extract_ocr_data_from_image")
@patch(f"{MODULE}.parse_text_free")
@patch("pandas.DataFrame.to_excel")
def test_processar_pdfs_ocr_free_ocr_ativo(mock_to_excel, mock_parse, mock_extract, mock_pdf_to_img, mock_listdir, contador, tmp_path):
    mock_listdir.return_value = ["a.pdf"]
    mock_pdf_to_img.return_value = ["img1"]
    mock_extract.return_value = ("texto livre", 90)
    mock_parse.return_value = [["01/01/2020", "123", "descrição", 1, 10, "D", "conta", 100]]
    df = contador.processar_pdfs_ocr_free(str(tmp_path), usar_ocr=True)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# Testar processar_cfop_pdfs com OCR desativado
def test_processar_cfop_pdfs_ocr_desativado(contador, tmp_path):
    df = contador.processar_cfop_pdfs(str(tmp_path), usar_ocr=False)
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# Testar processar_cfop_pdfs com OCR ativo e mocks
@patch(f"{MODULE}.pdf_to_images")
@patch(f"{MODULE}.extract_ocr_data_from_image")
@patch(f"{MODULE}.preprocess_cfop_image")
@patch(f"{MODULE}.extrair_cfop_valores")
@patch("pandas.DataFrame.to_excel")
def test_processar_cfop_pdfs_ocr_ativo(mock_to_excel, mock_extrair, mock_preprocess, mock_extract, mock_pdf_to_img, contador, tmp_path):
    pdf_file = tmp_path / "arquivo.pdf"
    pdf_file.write_text("dummy")
    mock_pdf_to_img.return_value = [MagicMock()]
    mock_extract.return_value = ("texto", None)
    mock_preprocess.return_value = MagicMock()
    mock_extrair.return_value = [{"campo": 1}]
    df = contador.processar_cfop_pdfs(str(tmp_path), usar_ocr=True)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# Testar processar_dcomp_pdfs
@patch(f"{MODULE}.processar_dcomp")
def test_processar_dcomp_pdfs(mock_processar, contador):
    mock_processar.return_value = pd.DataFrame({"a": [1]})
    df = contador.processar_dcomp_pdfs("pasta", usar_ocr=True)
    assert isinstance(df, pd.DataFrame)


# Testar processar_dcomp_pdfs com exceção
@patch(f"{MODULE}.processar_dcomp")
def test_processar_dcomp_pdfs_erro(mock_processar, contador):
    mock_processar.side_effect = Exception("Erro no processamento")
    df = contador.processar_dcomp_pdfs("pasta", usar_ocr=True)
    assert df.empty


# Testar processar_dcomp_ipi_pdfs
@patch(f"{MODULE}.processor_dcomp_ipi")
def test_processar_dcomp_ipi_pdfs(mock_processor, contador):
    mock_processor.return_value = pd.DataFrame({"a": [1]})
    df = contador.processar_dcomp_ipi_pdfs("pasta", usar_ocr=False)
    assert isinstance(df, pd.DataFrame)


# Testar processar_dcomp_ipi_pdfs com exceção
@patch(f"{MODULE}.processor_dcomp_ipi")
def test_processar_dcomp_ipi_pdfs_erro(mock_processor, contador):
    mock_processor.side_effect = Exception("Erro")
    df = contador.processar_dcomp_ipi_pdfs("pasta", usar_ocr=False)
    assert df.empty


# Testar processar_recolhimentos_pdfs
@patch(f"{MODULE}.extrair_recolhimento_pdf")
def test_processar_recolhimentos_pdfs(mock_recolhimento, contador):
    mock_recolhimento.return_value = pd.DataFrame({"a": [1]})
    df = contador.processar_recolhimentos_pdfs("pasta", usar_ocr=False)
    assert isinstance(df, pd.DataFrame)


# Testar processar_recolhimentos_pdfs exceção
@patch(f"{MODULE}.extrair_recolhimento_pdf")
def test_processar_recolhimentos_pdfs_erro(mock_recolhimento, contador):
    mock_recolhimento.side_effect = Exception("Erro")
    df = contador.processar_recolhimentos_pdfs("pasta", usar_ocr=False)
    assert df.empty


# teste test_process_file_r11_r12
@patch(f"{MODULE}.generate_line")
@patch(f"{MODULE}.carregar_excel")
@patch(f"{MODULE}.validar_colunas_valores")
@patch(f"{MODULE}.formatar_dados")
def test_process_file_r11_r12(mock_formatar, mock_validar, mock_carregar, mock_generate_line, contador):
    df_mock = pd.DataFrame({
        'Tipo': ['TIPO_TESTE'],
        'CNPJ do Declarante': ['12345678000199'],
        'CNPJ do Estabelecimento Detentor do Crédito': ['98765432000188'],
        'Período de Apuração': ['062024'],
        'Decêndio/Quinzena do Período de Apuração': ['1'],
        'CFOP': ['5102'],
        'Operações com Crédito do Imposto - Base de Cálculo': [1000.123],
        'Operações com Crédito do Imposto - IPI Creditado': [200.456],
        'Operações sem Crédito do Imposto - Isentas ou Não Tributadas': [300.789],
        'Operações sem Crédito do Imposto - Outras': [400.1011],
    })

    for col in [
        'Operações com Crédito do Imposto - Base de Cálculo',
        'Operações com Crédito do Imposto - IPI Creditado',
        'Operações sem Crédito do Imposto - Isentas ou Não Tributadas',
        'Operações sem Crédito do Imposto - Outras'
    ]:
        df_mock[col] = df_mock[col].astype(float)

    mock_carregar.return_value = df_mock.copy()
    mock_validar.return_value = df_mock.copy()
    mock_formatar.return_value = (df_mock.copy(), None)

    mock_generate_line.side_effect = lambda row: f"linha formatada para {row['Tipo']}\n"

    original_apply = pd.DataFrame.apply

    def fake_apply(self, func, axis=0, *args, **kwargs):
        if axis == 1:
            return [func(row) for _, row in self.iterrows()]
        else:
            return original_apply(self, func, axis=axis, *args, **kwargs)

    with patch.object(pd.DataFrame, 'apply', new=fake_apply):
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                output_path = contador.process_file_r11_r12("arquivo.xlsx")
                assert isinstance(output_path, str)
                assert os.path.isfile(output_path)
                with open(output_path, "r") as f:
                    content = f.read()
                assert "linha formatada para TIPO_TESTE" in content
            finally:
                os.chdir(cwd)


# Testar métodos que devem capturar exceções e não propagar erro
def test_processar_e_classificar_unificado_erro(contador):
    with patch(f"{MODULE}.comparar_e_classificar_excel", side_effect=Exception("Erro")):
        result = contador.processar_e_classificar_unificado("p1", "a1", 0, "p2", "a2", 1, ["c1"], ["c2"], "dir")
        assert result is None


def test_consulta_cnpj_erro(contador):
    with patch(f"{MODULE}.consulta_cnpj", side_effect=Exception("Erro")):
        result = contador.consulta_cnpj()
        assert result is None


if __name__ == "__main__":
    pytest.main()