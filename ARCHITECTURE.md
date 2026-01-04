# 🏗️ Arquitetura do Sistema - Liturgia

Documentação técnica da arquitetura, componentes e design do Sistema Liturgia.

---

## 📋 Índice

1. [Visão Geral](#-visão-geral)
2. [Arquitetura de Alto Nível](#-arquitetura-de-alto-nível)
3. [Componentes Principais](#-componentes-principais)
4. [Modelo de Dados](#-modelo-de-dados)
5. [Fluxo de Requisições](#-fluxo-de-requisições)
6. [Stack Tecnológica](#-stack-tecnológica)
7. [Padrões de Design](#-padrões-de-design)
8. [Segurança](#-segurança)

---

## 🎯 Visão Geral

O Sistema Liturgia é uma **aplicação web monolítica** construída com Flask (Python), utilizando PostgreSQL como banco de dados principal e Redis para cache. A aplicação segue o padrão **MVC (Model-View-Controller)** adaptado para Flask.

### Características Arquiteturais

- **Monolito Modular** - Componentes bem separados mas em uma única aplicação
- **RESTful API** - Endpoints REST para integração
- **Server-Side Rendering** - Templates Jinja2 para renderização no servidor
- **Persistência com ORM** - SQLAlchemy para abstração de banco de dados
- **Containerização** - Docker para deploy consistente
- **Orquestração** - Docker Swarm para alta disponibilidade

---

## 🏛️ Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────────────────────┐
│                         USUÁRIO                              │
│                    (Navegador Web)                           │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   REVERSE PROXY                              │
│         (Traefik / Nginx / Apache)                           │
│           - SSL/TLS Termination                              │
│           - Load Balancing                                   │
│           - Rate Limiting                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  APLICAÇÃO WEB                               │
│                  (Flask + WSGI)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Web Layer                                │  │
│  │  - Rotas (app.py)                                    │  │
│  │  - Controllers                                       │  │
│  │  - Templates (Jinja2)                                │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │           Business Logic Layer                        │  │
│  │  - Models (SQLAlchemy)                               │  │
│  │  - Services                                          │  │
│  │  - Validators                                        │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │            Data Access Layer                          │  │
│  │  - ORM (SQLAlchemy)                                  │  │
│  │  - Database Models                                   │  │
│  │  - Migrations (Flask-Migrate)                        │  │
│  └──────────────────┬───────────────────────────────────┘  │
└────────────────────┬┴────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌────────────┐ ┌──────────────┐
│  PostgreSQL  │ │   Redis    │ │ File Storage │
│   Database   │ │   Cache    │ │   (Volumes)  │
│              │ │            │ │              │
│ - Liturgias  │ │ - Sessões  │ │ - PDFs       │
│ - Leituras   │ │ - Cache    │ │ - Uploads    │
│ - Orações    │ │            │ │              │
└──────────────┘ └────────────┘ └──────────────┘
```

---

## 🧩 Componentes Principais

### 1. Aplicação Flask (`app.py`)

**Responsabilidades:**
- Inicialização da aplicação
- Configuração de rotas
- Middleware e extensões
- Tratamento de erros
- Health checks

**Principais Rotas:**
```python
/                           # Home (redirect para /liturgia-diaria)
/liturgia-diaria           # Liturgia do dia
/liturgia-horas            # Liturgia das Horas
/missa-personalizada       # Criar missa personalizada
/personalizar-pdf          # Customizar PDF
/admin/*                   # Área administrativa
/api/*                     # Endpoints API REST
```

---

### 2. Modelos de Dados (`models/`)

#### `daily_liturgy.py` - Liturgia Diária
```python
class LiturgiaDaily:
    - get_for_date(date)
    - get_full_text()
    - add_liturgy_data(date, data)
```

#### `liturgy_hours.py` - Liturgia das Horas
```python
class LiturgiaHoras:
    - get_office_readings(date)
    - get_laudes(date)
    - get_terca(date)
    - get_sexta(date)
    - get_nona(date)
    - get_vesperas(date)
    - get_completas(date)
    - get_all_hours(date)
```

#### `custom_mass.py` - Missa Personalizada
```python
class CustomMass:
    - set_celebration(...)
    - set_readings(...)
    - set_part_content(part, content)
    - export_to_pdf(filename)
    - export_to_docx(filename)
    - get_full_text()
```

#### `db_models.py` - Modelos de Banco de Dados
```python
- LiturgicalColor      # Cores litúrgicas
- Celebration          # Celebrações
- Reading              # Leituras bíblicas
- Psalm                # Salmos responsoriais
- Prayer               # Orações litúrgicas
- DailyLiturgy        # Liturgia diária
- Antiphon            # Antífonas
- LiturgyHour         # Horas canônicas
- CustomMass          # Missas personalizadas
```

---

### 3. Templates (`templates/`)

Sistema de templates Jinja2 com herança:

```
base.html                    # Template base (navbar, footer)
├── daily_liturgy.html      # Liturgia diária
├── liturgy_hours.html      # Liturgia das horas
├── custom_mass_form.html   # Formulário de missa
├── custom_mass_preview.html # Preview da missa
├── customize_pdf.html      # Customização de PDF
└── admin/                  # Templates administrativos
    ├── admin.html
    ├── add_liturgy.html
    └── ...
```

---

### 4. Arquivos Estáticos (`static/`)

```
static/
├── css/
│   └── style.css          # Estilos customizados
├── js/
│   └── main.js            # JavaScript customizado
└── images/                # Imagens e ícones
```

---

### 5. Banco de Dados (PostgreSQL)

**Esquema Principal:**

```sql
-- Cores Litúrgicas
liturgical_colors (id, name, meaning)

-- Celebrações
celebrations (id, name, date, type, season, color_id)

-- Leituras
readings (id, reference, text, book, chapter, verses)

-- Salmos
psalms (id, number, reference, response, verses)

-- Orações
prayers (id, type, name, text, occasion)

-- Liturgia Diária
daily_liturgies (id, date, celebration_id, first_reading_id, 
                psalm_id, second_reading_id, gospel_id)

-- Horas Canônicas
liturgy_hours (id, date, hour_type, hymn, psalms, 
              reading, prayers)

-- Missas Personalizadas
custom_masses (id, name, date, user_id, parts_json)
```

---

### 6. Cache (Redis)

**Uso:**
- Cache de consultas frequentes
- Sessões de usuário
- Rate limiting

**Chaves:**
```
liturgy:daily:{date}           # Liturgia do dia
liturgy:hours:{date}:{hour}    # Hora canônica
celebration:{date}             # Celebração
```

---

## 📊 Modelo de Dados

### Diagrama de Entidades (Simplificado)

```
┌─────────────────┐
│ LiturgicalColor │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│  Celebration    │◄──────┐
└────────┬────────┘       │
         │ 1              │
         │                │
         │ N              │ 1
┌────────▼────────┐       │
│  DailyLiturgy   │───────┘
└────────┬────────┘
         │
         │ has many
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
    ▼         ▼        ▼        ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌────────┐
│Reading │ │Psalm │ │Prayer│ │Antiphon│
└────────┘ └──────┘ └──────┘ └────────┘
```

### Relacionamentos Principais

1. **Celebration → LiturgicalColor** (N:1)
   - Cada celebração tem uma cor litúrgica

2. **DailyLiturgy → Celebration** (N:1)
   - Cada liturgia diária está associada a uma celebração

3. **DailyLiturgy → Reading/Psalm/Prayer** (N:N)
   - Uma liturgia contém múltiplas leituras, salmos e orações

4. **LiturgyHour → Prayer/Psalm** (N:N)
   - Cada hora canônica contém orações e salmos específicos

---

## 🔄 Fluxo de Requisições

### Exemplo: Visualizar Liturgia do Dia

```
1. Usuário acessa /liturgia-diaria
   │
   ▼
2. Flask Router → daily_liturgy_route()
   │
   ▼
3. Controller verifica cache (Redis)
   │
   ├─► Cache Hit? → Retorna dados do cache
   │
   └─► Cache Miss? ↓
       │
       ▼
4. LiturgiaDaily.get_for_date(today)
   │
   ▼
5. SQLAlchemy Query → PostgreSQL
   │
   ├─► Query Celebration
   ├─► Query Readings
   ├─► Query Psalm
   └─► Query Prayers
   │
   ▼
6. Monta objeto Liturgy
   │
   ▼
7. Armazena em cache (Redis)
   │
   ▼
8. Renderiza template (Jinja2)
   │
   ▼
9. Retorna HTML para usuário
```

---

## 💻 Stack Tecnológica

### Backend

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| **Python** | 3.8+ | Linguagem principal |
| **Flask** | 3.0 | Framework web |
| **SQLAlchemy** | 3.1+ | ORM |
| **Flask-Migrate** | 4.0+ | Migrations |
| **psycopg2** | 2.9+ | Driver PostgreSQL |
| **Gunicorn** | 21.2+ | WSGI Server |

### Frontend

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| **HTML5** | - | Markup |
| **CSS3** | - | Estilos |
| **Bootstrap** | 5.x | Framework CSS |
| **JavaScript** | ES6+ | Interatividade |
| **Jinja2** | 3.1+ | Templates |

### Banco de Dados

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| **PostgreSQL** | 15+ | Banco principal |
| **Redis** | 7+ | Cache e sessões |

### Infraestrutura

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| **Docker** | 20+ | Containerização |
| **Docker Swarm** | - | Orquestração |
| **Apache** | 2.4+ | Web server |
| **mod_wsgi** | 4.9+ | WSGI adapter |
| **Traefik** | 2.x | Reverse proxy (opcional) |

### Bibliotecas Adicionais

- **ReportLab** - Geração de PDF
- **python-docx** - Geração de DOCX
- **python-dateutil** - Manipulação de datas
- **Flask-WTF** - Formulários

---

## 🎨 Padrões de Design

### 1. MVC (Model-View-Controller)

- **Model:** `models/*.py` - Lógica de dados
- **View:** `templates/*.html` - Apresentação
- **Controller:** Funções em `app.py` - Lógica de controle

### 2. Repository Pattern

Classes de modelo encapsulam acesso aos dados:
```python
class LiturgiaDaily:
    @staticmethod
    def get_for_date(date):
        # Acesso ao banco de dados encapsulado
```

### 3. Service Layer

Lógica de negócio separada dos controllers:
```python
# services/liturgy_service.py
def get_complete_liturgy(date):
    liturgy = LiturgiaDaily.get_for_date(date)
    # Lógica de negócio adicional
    return liturgy
```

### 4. Factory Pattern

Para criação de objetos complexos:
```python
class MassFactory:
    @staticmethod
    def create_epiphany_mass():
        mass = CustomMass()
        # Configuração específica
        return mass
```

### 5. Singleton Pattern

Para configurações globais:
```python
# db instance (SQLAlchemy)
db = SQLAlchemy()
```

---

## 🔐 Segurança

### Autenticação e Autorização

- **Flask Sessions** - Gerenciamento de sessão
- **Secret Key** - Assinatura de cookies
- **CSRF Protection** - Flask-WTF

### Proteção de Dados

- **SQL Injection** - SQLAlchemy ORM (parametrizado)
- **XSS** - Jinja2 auto-escaping
- **CSRF** - Tokens CSRF em formulários

### HTTPS/TLS

- **Traefik** - SSL automático com Let's Encrypt
- **Apache** - Suporte SSL/TLS nativo

### Variáveis Sensíveis

- **Environment Variables** - Configurações sensíveis
- **Docker Secrets** - Para deploy em produção
- **.gitignore** - Arquivos sensíveis não commitados

### Headers de Segurança

```python
# Configurado no Apache/Traefik
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

---

## 📦 Deploy e Escalabilidade

### Containerização

```
Docker Image → Base: python:3.11-slim
├── System Dependencies (Apache, PostgreSQL client)
├── Python Dependencies (requirements.txt)
├── Application Code
└── Entrypoint Script (init + Apache)
```

### Orquestração (Docker Swarm)

```
Stack: liturgia
├── Service: app (2+ replicas)
│   ├── Load Balanced
│   ├── Rolling Updates
│   └── Auto-restart
├── Service: postgres (1 replica)
│   └── Persistent Volume
└── Service: redis (1 replica)
    └── Persistent Volume
```

### Volumes Persistentes

```
- postgres-data    # Dados do PostgreSQL
- redis-data       # Dados do Redis
- storage-data     # Uploads e arquivos
- cache-data       # Cache de aplicação
```

---

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Aplicação
APP_NAME=Liturgia Católica
APP_ENV=production
APP_DEBUG=false
SECRET_KEY=<random-secret>

# Banco de Dados
DB_CONNECTION=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=liturgia_db
DB_USERNAME=postgres
DB_PASSWORD=<secure-password>

# Cache
REDIS_HOST=redis
REDIS_PORT=6379

# Storage
UPLOAD_FOLDER=/var/www/storage
```

---

## 📈 Monitoramento

### Health Checks

```python
@app.route('/health')
def health_check():
    # Verifica conectividade com PostgreSQL
    # Verifica conectividade com Redis
    return {'status': 'healthy'}
```

### Logs

```bash
# Application logs
/var/log/apache2/access.log
/var/log/apache2/error.log

# Docker logs
docker service logs liturgia_app
```

### Métricas

- **Resource Usage** - CPU, Memória via Docker stats
- **Request Rate** - Via logs do Apache
- **Database** - Queries lentas via PostgreSQL logs

---

## 🚀 Fluxo de Desenvolvimento

```
1. Desenvolvimento Local
   ├── Código em Python
   ├── Teste manual (python app.py)
   └── Commit para Git
   │
   ▼
2. Build Docker Image
   ├── GitHub Actions / Manual
   ├── Push para ghcr.io
   └── Tag: latest / version
   │
   ▼
3. Deploy
   ├── Pull nova imagem
   ├── Rolling update
   └── Verificação
```

---

## 📚 Referências

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)

---

**Última atualização:** 2026-01-04
**Versão:** 2.0
