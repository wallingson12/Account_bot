# 🧠 Account Bot

Automatize tarefas contábeis com o poder do Python. Este projeto une uma interface web em Django com autenticação via JWT a um conjunto robusto de ferramentas que agilizam rotinas como conciliação de planilhas, consulta de CNPJs, manipulação de arquivos XML e muito mais.

---

## 🚀 Funcionalidades

A classe `Contador` centraliza todas as ações automatizadas:

### 📊 Planilhas Excel

- **processar_e_classificar_unificado**  
  Realiza conciliação e classificação entre duas planilhas com base em colunas chave.

- **dividir_excel**  
  Divide uma planilha com base em valores de uma coluna, gerando múltiplos arquivos.

- **unificar_excel_da_pasta**  
  Une todos os arquivos `.xls` e `.xlsx` de uma pasta em um único arquivo consolidado.

---

### 🧾 Arquivos XML

- **mover_arquivos_esocial**  
  Move todos ou metade dos arquivos XML da pasta base para a pasta destino.

- **organizar_xml_por_data**  
  Lê a data de emissão dos XMLs (tags como `dhEmi`, `dEmi`, `perApur`) e os organiza em subpastas por ano ou mês/ano.

---

### 🗃️ Organização de Arquivos

- **limpar_arquivos_por_formato**  
  Remove arquivos que não possuem uma extensão específica em uma pasta.

- **mover_arquivos_por_extensao**  
  Move todos os arquivos com uma extensão desejada para uma nova pasta.

---

### 🧠 Consulta de Dados

- **consulta_cnpj**  
  Consulta dados cadastrais de CNPJs contidos em um arquivo Excel e salva os resultados em um novo arquivo.

---

## ⚙️ Tecnologias

- **Backend**: Django + Django REST Framework + SimpleJWT  
- **Manipulação de dados**: `pandas`, `openpyxl`  
- **Web scraping e requests**: `requests`, `xml.etree.ElementTree`, `re`, `shutil`  
- **Interface Web**: Django Templates com rotas estilizadas e protegidas

---

🔐 API REST com JWT
A aplicação expõe uma API REST para autenticação e integração programática usando JSON Web Tokens (JWT), com os seguintes endpoints:

Método	Endpoint	Descrição
POST	/api/token/	Gera tokens JWT (access e refresh)
POST	/api/token/refresh/	Atualiza o token de acesso usando o refresh
