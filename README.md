# 🧠 Account Bot

Automatize tarefas contábeis com o poder do Python.  
Este projeto une uma interface web em **Django** com autenticação via **JWT** a um conjunto robusto de ferramentas que agilizam rotinas como conciliação de planilhas, consulta de CNPJs, manipulação de arquivos XML e muito mais.

---

## 🚀 Funcionalidades

A classe `Contador` centraliza todas as ações automatizadas:

### 📊 Planilhas Excel
- **processar_e_classificar_unificado** — Concilia e classifica duas planilhas com base em colunas chave.  
- **dividir_excel** — Divide uma planilha em múltiplos arquivos com base em valores de uma coluna.  
- **unificar_excel_da_pasta** — Une todos os arquivos `.xls` e `.xlsx` de uma pasta em um único arquivo consolidado.  

### 🧾 Arquivos XML
- **mover_arquivos_esocial** — Move todos ou metade dos arquivos XML de uma pasta para outra.  
- **organizar_xml_por_data** — Lê a data de emissão dos XMLs (`dhEmi`, `dEmi`, `perApur`) e organiza em subpastas por ano ou mês/ano.  

### 🗃️ Organização de Arquivos
- **limpar_arquivos_por_formato** — Remove arquivos que não possuem uma extensão específica.  
- **mover_arquivos_por_extensao** — Move arquivos de uma extensão específica para outra pasta.  

### 📄 PDFs e OCR
- **processar_pdfs_dctf** — Extrai dados estruturados de PDFs DCTF.  
- **processar_fontes_pagadoras** — Extrai dados estruturados de PDFs de Fontes pagadoras.  
- **processar_darf_pdfs** — Extrai dados estruturados de PDFs de DARFs.  
- **processar_pdfs_ocr_free** — OCR genérico para PDFs livres.  
- **processar_cfop_pdfs** — Extrai valores CFOP de PDFs fiscais.  
- **processar_dcomp_pdfs** — Extrai dados estruturados de PDFs de DCOMP.  
- **processar_dcomp_ipi_pdfs** — Extrai dados estruturados de PDFs de Dcomp.  
- **processar_recolhimentos_pdfs** — Extrai dados estruturados de PDFs de extratos de recolhimentos.  

### 🧠 Consulta de Dados
- **consulta_cnpj** — Consulta dados cadastrais de CNPJs contidos em um arquivo Excel e salva o resultado em um novo arquivo.  

---
### 📄 Arquivos de texto
- **process_file_r11_r12** — Gera arquivo de importação na dcomp  

## ⚙️ Tecnologias
- **Backend**: Django + Django REST Framework + SimpleJWT  
- **Manipulação de dados**: `pandas`, `openpyxl`  
- **OCR e PDFs**: `pytesseract`, `pdfplumber`, `pdf2image`, `opencv-python`  
- **Web scraping e requests**: `requests`, `xml.etree.ElementTree`, `re`, `shutil`  
- **Interface Web**: Django Templates com rotas estilizadas e protegidas  

---

## 🔐 API REST com JWT

A aplicação expõe uma API REST para autenticação e integração programática usando JSON Web Tokens (JWT):

| Método | Endpoint              | Descrição                                    |
|--------|-----------------------|----------------------------------------------|
| POST   | `/api/token/`         | Gera tokens JWT (access e refresh)           |
| POST   | `/api/token/refresh/` | Atualiza o token de acesso usando o refresh  |

---

## ⚡ Guia Rápido

### 📥 Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/seuusuario/account-bot.git
cd account-bot

# 2. Criar e ativar ambiente virtual (opcional)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar a aplicação Django
python manage.py runserver
