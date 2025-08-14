# 🧠 Account Bot

Automatize tarefas contábeis com o poder do **Python**.  
Este projeto une uma interface web em **Django** com autenticação via **JWT** a um conjunto robusto de ferramentas que agilizam rotinas como conciliação de planilhas, consulta de CNPJs, manipulação de arquivos XML e muito mais.

---

## 🚀 Funcionalidades

A classe **`Contador`** centraliza todas as ações automatizadas:

### 📊 Planilhas Excel
- **processar_e_classificar_unificado**: concilia e classifica planilhas com base em colunas chave.  
- **dividir_excel**: divide uma planilha com base em valores de uma coluna, gerando múltiplos arquivos.  
- **unificar_excel_da_pasta**: une todos os arquivos Excel de uma pasta em um único arquivo consolidado.  

### 🧾 Arquivos XML
- **mover_arquivos_esocial**: move todos ou metade dos arquivos XML de uma pasta para outra.  
- **organizar_xml_por_data**: organiza XMLs em subpastas por ano ou mês/ano, com base na data de emissão.  

### 🗃️ Organização de Arquivos
- **limpar_arquivos_por_formato**: mantém apenas arquivos com a extensão desejada.  
- **mover_arquivos_por_extensao**: move arquivos para uma pasta de destino, evitando sobrescritas.  

### 🧠 Consulta de Dados
- **consulta_cnpj**: consulta dados cadastrais de CNPJs em uma planilha e gera resultado consolidado.  

### 📄 Processamento de PDFs
- **dividir_pdf**: divide PDFs em páginas.  
- **processamento OCR avançado**:  
  - DCTF (`processar_pdfs_dctf`)  
  - Fontes Pagadoras (`processar_fontes_pagadoras`)  
  - DARF (`processar_darf_pdfs`)  
  - OCR Livre (`processar_pdfs_ocr_free`)  
  - CFOP (`processar_cfop_pdfs`)  
  - DCOMP (`processar_dcomp_pdfs`)  
  - DCOMP IPI (`processar_dcomp_ipi_pdfs`)  
  - Recolhimentos (`processar_recolhimentos_pdfs`)  

> Todos os módulos suportam **OCR via Tesseract** e pré-processamento de imagens, garantindo extração precisa de dados.

### 📝 Processamento Especial R11/R12
- Geração de arquivos TXT a partir de planilhas Excel, com validação e formatação automática.

---

## ⚙️ Tecnologias

- **Backend:** Django + Django REST Framework + SimpleJWT  
- **Manipulação de dados:** pandas, openpyxl  
- **PDF & OCR:** pytesseract, pdf2image, OpenCV  
- **Web scraping & requests:** requests, xml.etree.ElementTree, shutil, re  
- **Interface Web:** Django Templates com rotas protegidas  
- **API REST:** endpoints JWT para autenticação

**Endpoints principais da API:**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST   | `/api/token/` | Gera tokens JWT (access e refresh) |
| POST   | `/api/token/refresh/` | Atualiza token de acesso usando refresh |

---

💡 Automatize suas rotinas contábeis com **Account Bot** e ganhe tempo em tarefas repetitivas.
