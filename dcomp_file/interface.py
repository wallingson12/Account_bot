import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from generator import RegistroIPI  # Nosso módulo modularizado
from tabular_dcomp_ipi import tabular_dcomp_pdf  # PDF -> Excel

# Instância do gerador
gerador = RegistroIPI()

def select_and_process_excel(process_func):
    # Abrir o diálogo de seleção de arquivo Excel
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        # Abrir o diálogo para selecionar o diretório de saída
        output_dir = filedialog.askdirectory(title="Selecione o diretório de saída")
        if output_dir:
            try:
                # Processa o arquivo Excel e gera o arquivo TXT
                output_path = process_func(file_path, output_dir)
                messagebox.showinfo("Sucesso", f"Arquivo TXT gerado com sucesso em {output_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo: {e}")
        else:
            messagebox.showwarning("Atenção", "Nenhum diretório de saída selecionado.")
    else:
        messagebox.showwarning("Atenção", "Nenhum arquivo Excel selecionado.")

def process_pdf_handler():
    # Abrir o diálogo de seleção de arquivo PDF
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        # Abrir o diálogo para salvar o arquivo Excel
        excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")],
                                                 initialfile="output.xlsx")
        if excel_path:
            try:
                # Processar PDF para Excel
                tabular_dcomp_pdf(pdf_path, excel_path)
                messagebox.showinfo("Sucesso", f"Dados extraídos e salvos com sucesso em {excel_path}!")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao processar o PDF: {e}")
        else:
            messagebox.showwarning("Atenção", "Nenhum caminho de salvamento para o Excel foi selecionado.")
    else:
        messagebox.showwarning("Atenção", "Nenhum arquivo PDF selecionado.")

# Configuração da interface
root = tk.Tk()
root.title("Dcomp para TXT")
root.configure(bg="#012229")

# Definindo o tamanho da janela
window_width = 450
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20, bg="#012229")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Carregando imagem, se disponível
try:
    img = Image.open("mcs.jpg")  # Certifique-se de que o caminho está correto
    img = img.resize((100, 100))
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(frame, image=img, bg="#04242b")
    img_label.image = img  # Para evitar que a imagem seja coletada pelo garbage collector
    img_label.pack(pady=5)
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")
    img_label = tk.Label(frame, text="Imagem não encontrada.", bg="#04242b", fg="#FFFFFF")
    img_label.pack(pady=5)

text_label = tk.Label(frame, text="TAX", bg="#04242b", fg="#FFFFFF", font=("Arial", 12, "bold"))
text_label.pack(pady=10)

# Botões
btn_specs = [
    ("R11 ou R12 - Livro apuração com CFOP", lambda: select_and_process_excel(gerador.processar_r11_r12)),
    ("R13 - Notas fiscais de entrada/saída", lambda: select_and_process_excel(gerador.processar_r13)),
    ("R15 - Notas fiscais de créditos extemporâneos", lambda: select_and_process_excel(gerador.processar_r15)),
    ("R21 - Livro registro de apuração após ressarcimento", lambda: select_and_process_excel(gerador.processar_r21)),
    ("Selecionar PDF da Dcomp", process_pdf_handler)
]

# Adicionando os botões na interface
for text, command in btn_specs:
    btn = tk.Button(frame, text=text, command=command, bg="#00d97d", bd=5, fg="#000000",
                    font=("Arial", 10, "bold"), relief="raised")
    btn.pack(pady=5)

root.mainloop()
