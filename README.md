# Radar de Vagas- Sistema Full-Stack de Monitoramento

O Radar de Vagas é um projeto pessoal de um sistema Full-Stack projetado para automatizar a busca e o monitoramento de vagas de emprego em tempo real. A aplicação permite cadastrar palavras-chave (termos de busca), realiza varreduras automatizadas (Web Scraping) e exibe os resultados em um Dashboard interativo e moderno.

---

## 📌 Arquitetura do Sistema

O projeto adota uma arquitetura Cliente-Servidor (SPA + REST API), dividindo claramente as responsabilidades entre a interface do usuário e o processamento de dados em segundo plano.

* **Front-end (Cliente):** Interface reativa desenvolvida em React, responsável por consumir a API e renderizar os dados dinamicamente.
* **Back-end (Servidor/API):** Construído com FastAPI para lidar com requisições assíncronas, acionar os scripts de varredura (Scraping) e gerenciar as rotas.
* **Banco de Dados:** SQLite, utilizado para persistir os termos de busca e o histórico de vagas encontradas, garantindo que não haja duplicatas.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

### Front-end
* **React (v18+)** - Biblioteca JavaScript para construção da interface.
* **Vite** - Build tool ultra-rápida para o ambiente de desenvolvimento.
* **Tailwind CSS** - Framework de CSS utilitário para a estilização do Dark Mode e responsividade.
* **Axios** - Cliente HTTP para realizar as requisições (GET/POST) à API.

### Back-end
* **Python (v3.10+)** - Linguagem principal do servidor e automação.
* **FastAPI** - Framework web de alta performance para a construção da REST API.
* **Uvicorn** - Servidor ASGI para rodar a aplicação Python.
* **SQLAlchemy / SQLite** - ORM e Banco de Dados para persistência local.

---

## ⚙️ Funcionalidades

* **Cadastro de Termos:** Adição de palavras-chave dinâmicas para guiar o robô de busca (Ex: "Infraestrutura", "Suporte", "Dados").
* **Gatilho de Varredura Integrado:** Botão de ação única que salva o termo e instantaneamente dispara a rotina de Web Scraping no Back-end.
* **Sanitização de Dados (Filtro VIP):** Tratamento feito diretamente no Front-end com Expressões Regulares (Regex) para limpar inconsistências de texto originadas dos sites de vagas.
* **Ordenação Inteligente:** As vagas recém-capturadas são ordenadas por ID e exibidas no topo do Dashboard automaticamente.
* **Design Responsivo e Dark Mode:** Interface focada na experiência do usuário (UX), adaptável para celulares, tablets e monitores Desktop.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter instalado em sua máquina:
* Node.js (Para rodar o React/Vite)
* Python 3 (Para rodar a API)
* Git

### Passo 1: Configurar e Rodar o Back-end (API)
Abra um terminal na pasta raiz do projeto e execute:

```bash
# 1. Crie o ambiente virtual
python -m venv venv

# 2. Ative o ambiente virtual (Windows)
venv\Scripts\activate

# 3. Instale as dependências
pip install fastapi uvicorn sqlalchemy axios

# 4. Inicie o servidor
uvicorn app.main:app --reload
```
A API estará rodando em: http://127.0.0.1:8000

### Passo 2: Configurar e Rodar o Front-end (React)
Abra um novo terminal (mantenha o terminal do Python rodando), entre na pasta do Front-end e execute:

```bash
# 1. Entre na pasta do frontend
cd frontend-react

# 2. Instale as dependências do Node
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev
```
O Dashboard estará disponível no seu navegador em: http://localhost:5173

---

## 📂 Estrutura Básica de Diretórios

```text
alerta-vagas/
├── app/                  # Código-fonte do Back-end (Python/FastAPI)
│   ├── main.py           # Ponto de entrada da API e rotas
│   └── ...
├── frontend-react/       # Código-fonte do Front-end (React/Vite)
│   ├── src/
│   │   ├── App.jsx       # Componente principal e chamadas HTTP
│   │   └── main.jsx
│   ├── tailwind.config.js
│   └── package.json
├── venv/                 # Ambiente virtual Python (Ignorado pelo Git)
├── .gitignore            # Regras de exclusão para o repositório
└── README.md             # Documentação do projeto
```

---

## 📤 Guia de Deploy: Como subir este projeto para o GitHub

Se precisar recriar ou atualizar este repositório no GitHub, siga os passos abaixo:

### 1. Criar o arquivo .gitignore
Antes de qualquer comando Git, crie um arquivo chamado `.gitignore` na raiz do projeto (`alerta-vagas/`) com o seguinte conteúdo para não subir arquivos pesados:

```text
# Ignorar ambiente virtual do Python
venv/
__pycache__/
*.pyc

# Ignorar pacotes do Node/React
node_modules/
dist/

# Ignorar banco de dados local
*.db
*.sqlite3
```

### 2. Comandos no Terminal (Raiz do projeto)
Execute os comandos abaixo na sequência:

```bash
# Inicializa o repositório local
git init

# Prepara todos os arquivos permitidos pelo .gitignore
git add .

# Cria o pacote com a mensagem oficial
git commit -m "Primeiro commit: Sistema Vagas Radar Full-Stack finalizado"

# Define a ramificação principal como main
git branch -M main

# Conecta ao repositório vazio criado no site do GitHub (Troque pelo seu link)
git remote add origin [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/emillyyorke/alerta-vagas.git)

# Envia os arquivos para a nuvem
git push -u origin main
```

---
*Projeto desenvolvido do zero para automação de processos, estudos de arquitetura Cliente-Servidor e integração de sistemas.*
