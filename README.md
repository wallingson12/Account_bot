<h1 align="center">🧠 Account Bot</h1>

<p align="center">
Automatize tarefas contábeis com <strong>Python</strong> de forma rápida e eficiente!
</p>

---

## 🚀 Funcionalidades Principais

A classe <code>Contador</code> centraliza todas as automações:

### 📊 Planilhas Excel
- 🟢 **Conciliação e Classificação** (`processar_e_classificar_unificado`)  
  Compara e classifica planilhas automaticamente com base em colunas-chave.
- 🟢 **Divisão de Planilhas** (`dividir_excel`)  
  Divide uma planilha em múltiplos arquivos com base nos valores de uma coluna.
- 🟢 **Unificação de Planilhas** (`unificar_excel_da_pasta`)  
  Une todos os arquivos Excel de uma pasta em um único arquivo consolidado.

### 🧾 Arquivos XML
- 🔵 **Movimentação de arquivos eSocial** (`mover_arquivos_esocial`)  
  Move todos ou metade dos arquivos XML de uma pasta para outra.
- 🔵 **Organização por Data** (`organizar_xml_por_data`)  
  Cria subpastas por ano ou mês/ano, com base na data de emissão (`dhEmi`, `dEmi`, `perApur`).

### 🗃️ Organização de Arquivos
- 🟡 **Limpeza por formato** (`limpar_arquivos_por_formato`)  
  Mantém apenas arquivos com extensões específicas.
- 🟡 **Movimentação por extensão** (`mover_arquivos_por_extensao`)  
  Move arquivos para pasta de destino, evitando sobrescritas.

### 🧠 Consulta de Dados
- 🟣 **Consulta de CNPJs** (`consulta_cnpj`)  
  Consulta automática de dados cadastrais em planilhas Excel.

### 📄 Processamento de PDFs
- 📝 **Divisão de PDFs** (`dividir_pdf`)  
- 🔹 **Processamento OCR avançado**:
  - DCTF (`processar_pdfs_dctf`)
  - Fontes Pagadoras (`processar_fontes_pagadoras`)
  - DARF (`processar_darf_pdfs`)
  - OCR Livre (`processar_pdfs_ocr_free`)
  - CFOP (`processar_cfop_pdfs`)
  - DCOMP (`processar_dcomp_pdfs`)
  - DCOMP IPI (`processar_dcomp_ipi_pdfs`)
  - Recolhimentos (`processar_recolhimentos_pdfs`)

> Todos os módulos suportam **OCR via Tesseract** e pré-processamento de imagens para extração precisa de dados.

### 📝 Processamento Especial R11/R12
- Geração automática de arquivos TXT a partir de planilhas Excel específicas, com validação e formatação.

---

## ⚙️ Tecnologias

- **Backend:** Django + Django REST Framework + SimpleJWT  
- **Manipulação de dados:** pandas, openpyxl  
- **PDF & OCR:** pytesseract, pdf2image, OpenCV  
- **Web scraping & requests:** requests, xml.etree.ElementTree, shutil, re  
- **Interface Web:** Django Templates com rotas protegidas e estilizadas  
- **API REST:** endpoints JWT para autenticação

**Endpoints principais da API:**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST   | `/api/token/` | Gera tokens JWT (access e refresh) |
| POST   | `/api/token/refresh/` | Atualiza token de acesso usando refresh |

---

<p align="center">
💡 <strong>Demonstre o poder da automação contábil e ganhe tempo com o Account Bot!</strong>
</p>
