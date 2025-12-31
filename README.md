# 🧠 Account Bot

Automatize tarefas contábeis com o poder do Python. Este projeto une uma interface web em Django com autenticação via JWT a um conjunto robusto de ferramentas que agilizam rotinas contábeis como processamento de PDFs fiscais, conciliação de planilhas, consulta de CNPJs, OCR de documentos e muito mais.

---

## 🚀 Funcionalidades Principais

A classe `Contador` centraliza todas as ações automatizadas:

### 📊 **Manipulação de Planilhas Excel**

- **`comparar_excel()`**  
  Realiza conciliação e classificação entre duas planilhas com base em colunas chave.
  
- **`dividir_excel()`**  
  Divide uma planilha com base em valores de uma coluna, gerando múltiplos arquivos.
  
- **`unificar_excel_da_pasta()`**  
  Une todos os arquivos `.xls` e `.xlsx` de uma pasta em um único arquivo consolidado.
  
- **`consulta_cnpj()`**  
  Consulta dados cadastrais de CNPJs contidos em um arquivo Excel via API.

### 📄 **Processamento de PDFs Fiscais (com OCR)**

- **`dctf()`**  
  Extrai dados de Declarações de Débitos e Créditos Tributários Federais (DCTF).
  
- **`darf()`**  
  Processa Documentos de Arrecadação da Receita Federal (DARF).
  
- **`fontes_pagadoras()`**  
  Extrai informações de fontes pagadoras de rendimentos.
  
- **`cfop()`**  
  Processa documentos com Código Fiscal de Operações e Prestações (CFOP).
  
- **`processar_dcomp_pdfs()`**  
  Extrai dados de Declaração de Compensação (DCOMP).
  
- **`dcomp_ipi()`**  
  Processa DCOMP específicos para IPI.
  
- **`recolhimentos()`**  
  Extrai informações de documentos de recolhimento.
  
- **`ocr_free()`**  
  OCR livre para processamento genérico de documentos PDF.

### 📁 **Organização de Arquivos**

- **`limpar_arquivos_por_formato()`**  
  Remove arquivos que não possuem uma extensão específica em uma pasta.
  
- **`mover_arquivos_por_extensao()`**  
  Move todos os arquivos com uma extensão desejada para uma nova pasta.
  
- **`mover_arquivos_esocial()`**  
  Move todos ou metade dos arquivos XML da pasta base para a pasta destino.
  
- **`organizar_xml_por_data()`**  
  Lê a data de emissão dos XMLs (tags como `dhEmi`, `dEmi`, `perApur`) e os organiza em subpastas por ano ou mês/ano.
  
- **`dividir_pdf()`**  
  Divide arquivos PDF em páginas individuais ou seções.

### 🧾 **Processamento de IPI**

- **`processar_r11_r12()`**  
  Gera arquivos txt para importação do Registro R11/R12 na dcomp de ressarcimento de IPI.
  
- **`processar_r13()`**  
  Gera arquivos txt para importação do Registro R13 na dcomp de ressarcimento de IPI.
  
- **`processar_r15()`**  
  Gera arquivos txt para importação do Registro R15 na dcomp de ressarcimento de IPI.
  
- **`processar_r21()`**  
  Gera arquivos txt para importação do Registro R21 na dcomp de ressarcimento de IPI.

---

### 🔐 **API REST com Autenticação JWT**
- Autenticação segura com JSON Web Tokens (JWT)
- Endpoints protegidos com tokens de acesso e refresh
- Integração com Django REST Framework

### **Processamento de Dados**
- **Pandas** - Manipulação de dados e Excel
- **Openpyxl** - Leitura/escrita de arquivos Excel
- **PyTesseract** - OCR para extração de texto de imagens
- **PDF2Image** - Conversão de PDF para imagens
- **TQDM** - Barras de progresso para processamentos longos

### **Manipulação de Arquivos**
- **Pathlib** - Gerenciamento de caminhos de arquivos
- **Shutil** - Operações de sistema de arquivos
- **xml.etree.ElementTree** - Processamento de XML

### **Requisitos de Sistema**
- **Tesseract OCR** instalado no sistema
- **Python 3.8+**

---

## 🔐 **API REST com JWT**

A aplicação expõe uma API REST para autenticação e integração programática:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/token/` | Gera tokens JWT (access e refresh) |
| POST | `/api/token/refresh/` | Atualiza o token de acesso usando o refresh token |

---

---

## ⚙️ **Configuração e Uso**

### **1. Instalação**

```bash
# Clone o repositório
git clone [seu-repositorio]

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o caminho do Tesseract OCR
# Edite config/config.py com o caminho correto

2. Configuração do Tesseract
# Em config/config.py
caminho_tesseract = "/usr/bin/tesseract"  # Linux
# ou
caminho_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Windows

📄 Licença
Este projeto está licenciado sob a licença MIT.
