import os
import pandas as pd
from .layouts import LAYOUT_R11_R12, LAYOUT_R13, LAYOUT_R15, LAYOUT_R21
from dcomp_file.preprocess import format_record
from .formatter import format_field

class RegistroIPI:

    def format_row_to_txt_line(self, row, layout):
        """
        Converte uma linha do DataFrame em uma linha de texto formatada.

        Args:
            row (pd.Series): Linha do DataFrame.
            layout (list): Layout de campos com posições e tipos.

        Returns:
            str: Linha formatada para o TXT, com '\n' ao final.
        """
        line = ''
        if 'Período de Apuração' in row:
            periodo = str(row['Período de Apuração']).zfill(6)
            mes = periodo[:2]
            ano = periodo[2:]
        else:
            mes = ano = ''

        for campo, inicio, fim, tipo in layout:
            if campo is None:
                value = ''
            elif campo == 'MES':
                value = mes
            elif campo == 'ANO':
                value = ano
            else:
                value = row[campo]
            line += format_field(value, inicio, fim, tipo)
        return line + '\n'

    def _process_excel_to_txt(self, file_path, output_dir, layout, pre=None):
        """
        Processa um Excel e gera um TXT conforme o layout.

        Args:
            file_path (str): Caminho do Excel de entrada.
            output_dir (str): Diretório de saída do TXT.
            layout (list): Layout de campos.
            pre (callable, opcional): Função de pré-processamento do DataFrame.

        Returns:
            str: Caminho do TXT gerado.
        """
        # Use 'openpyxl' explicitamente para garantir que o arquivo .xlsx seja lido corretamente
        df = pd.read_excel(file_path, engine='openpyxl')  # Alteração aqui

        if pre:
            df = pre(df)
        lines = df.apply(lambda r: self.format_row_to_txt_line(r, layout), axis=1)

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{df['Tipo'].iloc[0]}.txt")
        with open(output_path, 'w') as f:
            f.writelines(lines)
        return output_path

    def processar_r11_r12(self, file_path, output_dir):
        """Processa registros R11/R12 e gera TXT."""
        return self._process_excel_to_txt(file_path, output_dir, LAYOUT_R11_R12)

    def processar_r13(self, file_path, output_dir):
        """Processa registros R13 e gera TXT."""
        return self._process_excel_to_txt(file_path, output_dir, LAYOUT_R13, lambda df: format_record(df, 'r13'))

    def processar_r15(self, file_path, output_dir):
        """Processa registros R15 e gera TXT."""
        return self._process_excel_to_txt(file_path, output_dir, LAYOUT_R15, lambda df: format_record(df, 'r15'))

    def processar_r21(self, file_path, output_dir):
        """Processa registros R21 e gera TXT."""
        return self._process_excel_to_txt(file_path, output_dir, LAYOUT_R21)
