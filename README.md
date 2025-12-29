# 🧠 Account Bot

Automatize tarefas contábeis com o poder do Python. Este projeto une uma interface web em Django com autenticação via JWT a um conjunto robusto de ferramentas que agilizam rotinas contábeis como processamento de PDFs fiscais, conciliação de planilhas, consulta de CNPJs, OCR de documentos e muito mais.

---

## 🚀 Funcionalidades Principais

A classe `Contador` centraliza todas as ações automatizadas:

### 📊 **Manipulação de Planilhas Excel**

- **`processar_e_classificar_unificado()`**  
  Realiza conciliação e classificação entre duas planilhas com base em colunas chave.
  
- **`dividir_excel()`**  
  Divide uma planilha com base em valores de uma coluna, gerando múltiplos arquivos.
  
- **`unificar_excel_da_pasta()`**  
  Une todos os arquivos `.xls` e `.xlsx` de uma pasta em um único arquivo consolidado.
  
- **`consulta_cnpj()`**  
  Consulta dados cadastrais de CNPJs contidos em um arquivo Excel via API da Receita Federal.

### 📄 **Processamento de PDFs Fiscais (com OCR)**

- **`processar_pdfs_dctf()`**  
  Extrai dados de Declarações de Débitos e Créditos Tributários Federais (DCTF) usando OCR.
  
- **`processar_darf_pdfs()`**  
  Processa Documentos de Arrecadação da Receita Federal (DARF) com reconhecimento de texto.
  
- **`processar_fontes_pagadoras()`**  
  Extrai informações de fontes pagadoras de rendimentos.
  
- **`processar_cfop_pdfs()`**  
  Processa documentos com Código Fiscal de Operações e Prestações (CFOP).
  
- **`processar_dcomp_pdfs()`**  
  Extrai dados de Declaração de Compensação (DCOMP).
  
- **`processar_dcomp_ipi_pdfs()`**  
  Processa DCOMP específicos para IPI.
  
- **`processar_recolhimentos_pdfs()`**  
  Extrai informações de documentos de recolhimento.
  
- **`processar_pdfs_ocr_free()`**  
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
  Gera arquivos para Registro R11/R12 do IPI.
  
- **`processar_r13()`**  
  Processa Registro R13 do IPI.
  
- **`processar_r15()`**  
  Processa Registro R15 do IPI.
  
- **`processar_r21()`**  
  Processa Registro R21 do IPI.

---

## 🛠️ **Tecnologias Utilizadas**

### **Backend & API**
- **Django** + **Django REST Framework** + **SimpleJWT**
- Autenticação via tokens JWT (access/refresh)

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
