# 📦 Instalação Local - Sistema Liturgia

Guia completo e detalhado para instalação e execução do Sistema Liturgia em ambiente local (desenvolvimento e testes).

---

## 📋 Índice

1. [Pré-requisitos](#-pré-requisitos)
2. [Instalação Rápida](#-instalação-rápida)
3. [Instalação Detalhada](#-instalação-detalhada)
4. [Configuração](#-configuração)
5. [Executando a Aplicação](#-executando-a-aplicação)
6. [Testando a Instalação](#-testando-a-instalação)
7. [Troubleshooting](#-troubleshooting)

---

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

### Obrigatórios
- **Python 3.8 ou superior** ([Download](https://www.python.org/downloads/))
- **pip** (gerenciador de pacotes Python - normalmente vem com Python)
- **Git** ([Download](https://git-scm.com/downloads))

### Opcionais (mas recomendados)
- **PostgreSQL 15** (para usar banco de dados PostgreSQL)
- **Redis** (para cache e sessões)
- **virtualenv** ou **venv** (para ambiente virtual Python)

### Verificar Instalações

```bash
# Verificar Python
python --version
# Deve mostrar: Python 3.8.x ou superior

# Verificar pip
pip --version

# Verificar Git
git --version
```

---

## ⚡ Instalação Rápida

Para quem quer começar rapidamente (modo desenvolvimento com SQLite):

```bash
# 1. Clonar o repositório
git clone https://github.com/josemaeldon/liturgia.git
cd liturgia

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar a aplicação
python app.py
```

✅ Pronto! Acesse: http://localhost:5000

---

## 🔧 Instalação Detalhada

### Passo 1: Clonar o Repositório

```bash
# Clone o repositório
git clone https://github.com/josemaeldon/liturgia.git

# Entre no diretório
cd liturgia

# Verificar estrutura
ls -la
```

Você deve ver arquivos como: `app.py`, `requirements.txt`, `docker-compose.yml`, etc.

---

### Passo 2: Criar Ambiente Virtual (Recomendado)

Usar um ambiente virtual isola as dependências do projeto:

#### No Linux/Mac:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Você verá (venv) no início do prompt
```

#### No Windows:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Você verá (venv) no início do prompt
```

---

### Passo 3: Instalar Dependências

```bash
# Atualizar pip (recomendado)
pip install --upgrade pip

# Instalar todas as dependências do projeto
pip install -r requirements.txt
```

**O que será instalado:**
- Flask (framework web)
- SQLAlchemy (ORM para banco de dados)
- psycopg2 (driver PostgreSQL)
- Flask-Migrate (migrations de banco)
- ReportLab (geração de PDF)
- python-docx (geração de DOCX)
- E outras dependências...

Aguarde a instalação completar. Pode levar alguns minutos.

---

### Passo 4: Configurar Variáveis de Ambiente

#### Opção A: SQLite (Mais Simples - Recomendado para Dev)

Não precisa de configuração adicional! A aplicação usa SQLite por padrão.

#### Opção B: PostgreSQL (Recomendado para Produção)

Se quiser usar PostgreSQL localmente:

1. **Instale o PostgreSQL** (se ainda não tiver)
   - Linux: `sudo apt install postgresql postgresql-contrib`
   - Mac: `brew install postgresql`
   - Windows: [Download](https://www.postgresql.org/download/windows/)

2. **Crie o banco de dados:**

```bash
# Entre no PostgreSQL
sudo -u postgres psql

# No prompt do PostgreSQL, execute:
CREATE DATABASE liturgia_db;
CREATE USER liturgia_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE liturgia_db TO liturgia_user;
\q
```

3. **Configure as variáveis de ambiente:**

**Linux/Mac:**
```bash
export DB_CONNECTION=pgsql
export DB_HOST=localhost
export DB_PORT=5432
export DB_DATABASE=liturgia_db
export DB_USERNAME=liturgia_user
export DB_PASSWORD=sua_senha_aqui
export SECRET_KEY=dev-secret-key-change-in-production
export FLASK_ENV=development
export FLASK_DEBUG=true
```

**Windows (PowerShell):**
```powershell
$env:DB_CONNECTION="pgsql"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_DATABASE="liturgia_db"
$env:DB_USERNAME="liturgia_user"
$env:DB_PASSWORD="sua_senha_aqui"
$env:SECRET_KEY="dev-secret-key-change-in-production"
$env:FLASK_ENV="development"
$env:FLASK_DEBUG="true"
```

**Ou crie um arquivo `.env`** (mais conveniente):

```bash
# Copie o exemplo
cp .env.example .env

# Edite o arquivo .env
nano .env  # ou use seu editor favorito
```

No arquivo `.env`, configure:
```env
DB_CONNECTION=pgsql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=liturgia_db
DB_USERNAME=liturgia_user
DB_PASSWORD=sua_senha_aqui
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=true
```

---

### Passo 5: Inicializar o Banco de Dados

```bash
# Inicializar o banco de dados e criar tabelas
python init_db.py
```

Este script irá:
- ✅ Criar todas as tabelas necessárias
- ✅ Inserir dados iniciais (cores litúrgicas, celebrações exemplo)
- ✅ Preparar o sistema para uso

Você deve ver mensagens como:
```
Initializing liturgical colors...
  Added color: verde
  Added color: branco
...
Database initialized successfully!
```

---

## 🚀 Executando a Aplicação

### Modo Desenvolvimento (Flask Built-in Server)

```bash
# Simples - servidor de desenvolvimento Flask
python app.py
```

A aplicação estará disponível em:
- 🌐 **URL:** http://localhost:5000
- 🔍 **Debug:** Habilitado (auto-reload em mudanças)

### Modo Produção Local (Gunicorn)

Para simular ambiente de produção:

```bash
# Instalar Gunicorn (se ainda não tiver)
pip install gunicorn

# Executar com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Parâmetros:
- `-w 4`: 4 workers (processos)
- `-b 0.0.0.0:5000`: Bind na porta 5000
- `app:app`: módulo:aplicação

---

## ✅ Testando a Instalação

### 1. Acesse a Interface Web

Abra seu navegador e acesse:
```
http://localhost:5000
```

Você deve ver a página inicial do Sistema Liturgia.

### 2. Teste os Endpoints

#### Liturgia do Dia:
```
http://localhost:5000/liturgy/daily
```

#### Liturgia das Horas:
```
http://localhost:5000/liturgy/hours
```

#### Criar Missa Personalizada:
```
http://localhost:5000/mass/custom
```

### 3. Execute os Exemplos Python

O projeto inclui vários scripts de exemplo:

```bash
# Missa completa da Epifania
python examples/example_epifania.py

# Liturgia diária
python examples/example_daily_liturgy.py

# Liturgia das Horas
python examples/example_liturgy_hours.py

# Todas as 7 horas canônicas
python examples/example_all_hours.py

# Todas as partes da Missa
python examples/example_all_mass_parts.py

# Criar missa personalizada
python examples/example_custom_mass.py
```

### 4. Teste a API

```bash
# Obter liturgia do dia (formato JSON)
curl http://localhost:5000/api/liturgy/daily/2026-01-06

# Obter Laudes
curl http://localhost:5000/api/liturgy/hours/laudes/2026-01-06
```

---

## 🐛 Troubleshooting

### Problema: ModuleNotFoundError

**Erro:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solução:**
```bash
# Certifique-se de que está no ambiente virtual (se usando)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Reinstale as dependências
pip install -r requirements.txt
```

---

### Problema: Erro de Conexão com PostgreSQL

**Erro:**
```
psycopg2.OperationalError: could not connect to server
```

**Soluções:**

1. **Verificar se PostgreSQL está rodando:**
```bash
# Linux
sudo systemctl status postgresql

# Mac
brew services list

# Iniciar se não estiver rodando
sudo systemctl start postgresql  # Linux
brew services start postgresql   # Mac
```

2. **Verificar credenciais:**
```bash
# Testar conexão manualmente
psql -h localhost -U liturgia_user -d liturgia_db
```

3. **Verificar variáveis de ambiente:**
```bash
echo $DB_HOST
echo $DB_DATABASE
echo $DB_USERNAME
```

---

### Problema: Porta 5000 já em uso

**Erro:**
```
OSError: [Errno 48] Address already in use
```

**Soluções:**

1. **Use outra porta:**
```bash
# Edite app.py e altere a porta
# Ou execute assim:
FLASK_RUN_PORT=8000 python app.py
```

2. **Ou mate o processo na porta 5000:**
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID [PID] /F
```

---

### Problema: Erro ao criar tabelas

**Erro:**
```
sqlalchemy.exc.ProgrammingError: relation "liturgical_color" already exists
```

**Solução:**

O banco já foi inicializado. Se quiser recomeçar:

```bash
# PostgreSQL: Dropar e recriar o banco
psql -U postgres -c "DROP DATABASE liturgia_db;"
psql -U postgres -c "CREATE DATABASE liturgia_db;"

# SQLite: Deletar o arquivo
rm liturgia.db

# Depois, reinicialize
python init_db.py
```

---

### Problema: Permissões de arquivo

**Erro (Linux/Mac):**
```
PermissionError: [Errno 13] Permission denied
```

**Solução:**
```bash
# Dar permissões aos diretórios necessários
chmod -R 755 /tmp/liturgia_pdfs
chmod +x entrypoint.sh
```

---

### Problema: Dependências não instalam

**Erro:**
```
error: Microsoft Visual C++ 14.0 is required
```

**Solução (Windows):**
1. Instale o [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Ou use versões binárias pré-compiladas:
```bash
pip install --only-binary :all: psycopg2-binary
```

---

## 📊 Estrutura de Diretórios Locais

Após a instalação, você terá:

```
liturgia/
├── venv/                    # Ambiente virtual (se criado)
├── app.py                   # Aplicação Flask
├── init_db.py              # Script de inicialização
├── requirements.txt        # Dependências
├── .env                    # Variáveis de ambiente (criar)
├── models/                 # Modelos de dados
├── templates/              # Templates HTML
├── static/                 # CSS, JS, imagens
├── examples/               # Scripts de exemplo
└── liturgia.db            # Banco SQLite (se usar SQLite)
```

---

## 🔄 Atualizar a Aplicação

Para atualizar para a versão mais recente:

```bash
# 1. Parar a aplicação (Ctrl+C)

# 2. Atualizar o código
git pull origin main

# 3. Atualizar dependências
pip install -r requirements.txt --upgrade

# 4. Atualizar banco de dados (migrations)
flask db upgrade

# 5. Reiniciar a aplicação
python app.py
```

---

## 🔐 Segurança em Desenvolvimento

Mesmo em desenvolvimento local, siga boas práticas:

1. **Não compartilhe o arquivo `.env`**
2. **Use senhas diferentes do exemplo**
3. **Mantenha `FLASK_DEBUG=false` quando não estiver desenvolvendo**
4. **Não exponha a aplicação para a internet sem firewall**

---

## 📚 Próximos Passos

Agora que você tem a aplicação rodando localmente:

1. 📖 Leia o [Guia de Uso (USAGE.md)](USAGE.md)
2. 🎯 Explore os exemplos na pasta `examples/`
3. 🔧 Personalize as configurações no `.env`
4. 🐳 Quando estiver pronto, veja o [Guia de Deploy no Portainer](INSTALL_PORTAINER.md)

---

## 💡 Dicas de Desenvolvimento

### Hot Reload (Auto-restart)

O Flask já possui hot reload habilitado em modo debug. Basta salvar os arquivos e a aplicação reinicia automaticamente.

### Logs Detalhados

```bash
# Habilitar logs verbosos
export FLASK_DEBUG=true
python app.py
```

### Usar Shell Interativo

```bash
# Abrir shell Flask para testar modelos
flask shell

# Dentro do shell:
>>> from models.daily_liturgy import LiturgiaDaily
>>> liturgy = LiturgiaDaily.get_for_date("2026-01-06")
>>> print(liturgy)
```

### Executar Testes

```bash
# Se houver testes no projeto
python -m pytest
```

---

## 🆘 Precisa de Ajuda?

- 📖 Leia a [documentação completa](README.md)
- 🐛 Abra uma [issue no GitHub](https://github.com/josemaeldon/liturgia/issues)
- 💬 Consulte os [exemplos práticos](examples/)

---

**Instalação local concluída com sucesso! 🎉**

Próximo passo: [Como usar a aplicação (USAGE.md)](USAGE.md) ou [Deploy em produção (INSTALL_PORTAINER.md)](INSTALL_PORTAINER.md)
