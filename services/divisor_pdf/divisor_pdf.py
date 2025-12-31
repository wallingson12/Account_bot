from PyPDF2 import PdfReader, PdfWriter
import os

def dividir_pdf(input_pdf_path):
    # Abre o PDF original
    reader = PdfReader(input_pdf_path)
    total_paginas = len(reader.pages)

    print(f"O PDF tem {total_paginas} páginas.")
    escolha = input("Quer dividir por (1) página ou (2) número específico de páginas? Digite 1 ou 2: ").strip()

    # Extrai o nome do arquivo para salvar os novos arquivos
    nome_base = os.path.splitext(os.path.basename(input_pdf_path))[0]

    if escolha == '1':
        # Divide página por página
        for i in range(total_paginas):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            output_filename = f"{nome_base}_pagina_{i+1}.pdf"
            with open(output_filename, "wb") as out_file:
                writer.write(out_file)
            print(f"Salvo: {output_filename}")

    elif escolha == '2':
        while True:
            try:
                n = int(input("Digite o número de páginas para cada arquivo (ex: 20): "))
                if n < 1:
                    print("Por favor, digite um número maior que zero.")
                    continue
                break
            except ValueError:
                print("Digite um número válido.")

        # Divide em blocos de n páginas
        for start in range(0, total_paginas, n):
            writer = PdfWriter()
            end = min(start + n, total_paginas)
            for i in range(start, end):
                writer.add_page(reader.pages[i])
            output_filename = f"{nome_base}_paginas_{start+1}_a_{end}.pdf"
            with open(output_filename, "wb") as out_file:
                writer.write(out_file)
            print(f"Salvo: {output_filename}")

    else:
        print("Opção inválida. Execute o programa novamente.")

if __name__ == "__main__":
    caminho_pdf = input("Digite o caminho do arquivo PDF: ").strip()
    if os.path.isfile(caminho_pdf):
        dividir_pdf(caminho_pdf)
    else:
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")