# 🕊️ Liturgia - Sistema Completo de Liturgia Católica

Sistema web moderno e completo para gerenciamento, consulta e personalização de liturgias católicas.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

---

## 📖 Índice

> 📚 **[Índice Completo da Documentação →](DOCS_INDEX.md)** - Guia de toda a documentação disponível

- [Visão Geral](#-visão-geral)
- [Características](#-características)
- [Instalação](#-instalação)
- [Uso Básico](#-uso-básico)
- [Documentação](#-documentação)
- [Tecnologias](#-tecnologias)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O **Sistema Liturgia** é uma aplicação web completa desenvolvida em Python/Flask que oferece:

- 📅 **Liturgia Diária** - Leituras e orações do dia
- ⏰ **Liturgia das Horas** - Todas as 7 horas canônicas completas
- ⛪ **Personalização de Missas** - 77 partes personalizáveis da estrutura completa da Missa
- 🎨 **Interface Moderna** - UI responsiva e intuitiva
- 🗄️ **Banco de Dados PostgreSQL** - Gestão robusta de dados litúrgicos
- 🐳 **Deploy Simplificado** - Pronto para Docker e Portainer

---

## ✨ Características

### Liturgia Diária
- Acesso completo às leituras do dia
- Primeira Leitura, Salmo Responsorial, Segunda Leitura
- Evangelho e Aleluia
- Cores litúrgicas e tempo litúrgico

### Liturgia das Horas Completa
Todas as 7 horas canônicas do Ofício Divino:
- **Ofício das Leituras** (Matutino)
- **Laudes** (Oração da Manhã)
- **Hora Média**: Terça (9h), Sexta (12h), Nona (15h)
- **Vésperas** (Oração da Tarde)
- **Completas** (Oração da Noite)

### Personalização de Missas
77 partes personalizáveis cobrindo toda a estrutura da Missa:
- **Ritos Iniciais** (12 partes)
- **Liturgia da Palavra** (14 partes)
- **Liturgia Eucarística** (43 partes)
- **Ritos Finais** (8 partes)

### Funcionalidades Técnicas
- ✅ Interface web responsiva e moderna
- ✅ API RESTful para integração
- ✅ Exportação para PDF e DOCX
- ✅ Sistema de cache com Redis
- ✅ Autenticação e permissões
- ✅ Migrations automáticas de banco de dados
- ✅ Health checks e monitoramento

---

## 🚀 Instalação

Escolha o método de instalação mais adequado para sua necessidade:

### 📦 Instalação Local (Desenvolvimento)

Para desenvolvimento local e testes:

👉 **[Guia Completo de Instalação Local](INSTALL_LOCAL.md)**

**Resumo rápido:**
```bash
git clone https://github.com/josemaeldon/liturgia.git
cd liturgia
pip install -r requirements.txt
python app.py
```
Acesse: http://localhost:5000

---

### 🐳 Instalação com Portainer (Produção)

Para deploy em produção usando Portainer:

👉 **[Guia Completo de Instalação no Portainer](INSTALL_PORTAINER.md)**

**Resumo rápido:**
1. Acesse seu Portainer
2. Crie uma nova Stack
3. Cole o conteúdo do `docker-compose.yml`
4. Configure as variáveis de ambiente
5. Deploy!

---

### ⚡ Outras Opções de Deploy

- 🐋 **[Docker Deployment](DOCKER_DEPLOYMENT.md)** - Deploy rápido com Docker
- 📖 **[Deploy Manual](DEPLOYMENT.md)** - Gunicorn, Nginx, Systemd
- 🗄️ **[PostgreSQL + Apache](POSTGRES_APACHE_DEPLOYMENT.md)** - Stack completa

---

## 💻 Uso Básico

### Interface Web

Após a instalação, acesse a interface web:

```
http://seu-servidor/
```

### API Python

```python
from models.daily_liturgy import LiturgiaDaily
from models.liturgy_hours import LiturgiaHoras
from models.custom_mass import CustomMass

# Liturgia do dia
liturgy = LiturgiaDaily.get_for_date("2026-01-06")
print(liturgy.get_full_text())

# Liturgia das Horas
laudes = LiturgiaHoras.get_laudes("2026-01-06")
print(laudes.format())

# Missa Personalizada
mass = CustomMass()
mass.set_celebration("Solenidade da Epifania")
mass.export_to_pdf("missa.pdf")
```

### Exemplos Práticos

Execute os exemplos incluídos no projeto:

```bash
python examples/example_epifania.py          # Missa completa da Epifania
python examples/example_daily_liturgy.py      # Liturgia diária
python examples/example_liturgy_hours.py      # Horas canônicas
python examples/example_all_hours.py          # Todas as 7 horas
python examples/example_custom_mass.py        # Missa personalizada
```

---

## 📚 Documentação

> 📚 **[Índice Completo da Documentação →](DOCS_INDEX.md)** - Acesse o índice completo com todos os guias

### 🚀 Guias de Instalação
- 📦 **[INSTALL_LOCAL.md](INSTALL_LOCAL.md)** - Instalação local detalhada (desenvolvimento)
- 🐳 **[INSTALL_PORTAINER.md](INSTALL_PORTAINER.md)** - Instalação no Portainer passo a passo (produção)
- 🐋 **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Deploy com Docker CLI
- 📘 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy manual (Gunicorn, Nginx)

### 📖 Guias de Uso
- 📖 **[USAGE.md](USAGE.md)** - Guia completo de uso da API Python
- 🌐 **[WEB_README.md](WEB_README.md)** - Interface web e funcionalidades

### 🔧 Documentação Técnica
- 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura do sistema
- 🗄️ **[DATABASE_INTEGRATION.md](DATABASE_INTEGRATION.md)** - Integração com PostgreSQL
- ⚙️ **[.env.example](.env.example)** - Exemplo de variáveis de ambiente
- 🐳 **[docker-compose.yml](docker-compose.yml)** - Configuração Docker

---

## 🏗️ Estrutura do Projeto

```
liturgia/
├── app.py                    # Aplicação Flask principal
├── init_db.py               # Script de inicialização do banco
├── models/                  # Modelos de dados
│   ├── daily_liturgy.py    # Liturgia diária
│   ├── liturgy_hours.py    # Liturgia das horas
│   ├── custom_mass.py      # Missas personalizadas
│   └── db_models.py        # Modelos SQLAlchemy
├── templates/              # Templates HTML
├── static/                 # Arquivos estáticos (CSS, JS)
├── examples/               # Exemplos de uso
├── requirements.txt        # Dependências Python
├── Dockerfile             # Imagem Docker
├── docker-compose.yml     # Orquestração Docker
└── docs/                  # Documentação adicional
```

---

## 🛠️ Tecnologias

### Backend
- **Python 3.8+** - Linguagem principal
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Migrate** - Migrations de banco de dados

### Banco de Dados
- **PostgreSQL 15** - Banco de dados principal
- **Redis 7** - Cache e sessões

### Frontend
- **HTML5/CSS3** - Interface web
- **JavaScript** - Interatividade
- **Bootstrap** - Framework CSS responsivo

### Infraestrutura
- **Docker** - Containerização
- **Apache/mod_wsgi** - Servidor web de produção
- **Gunicorn** - Servidor WSGI alternativo
- **Portainer** - Gerenciamento de containers

### Bibliotecas Adicionais
- **ReportLab** - Geração de PDF
- **python-docx** - Geração de DOCX
- **python-dateutil** - Manipulação de datas

---

## 👥 Contribuindo

Contribuições são muito bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes
- Siga as convenções de código Python (PEP 8)
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Mantenha commits claros e descritivos

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

Você é livre para usar, modificar e distribuir este software, desde que mantenha o aviso de copyright e a licença.

---

## 🔗 Links Úteis

- [Documentação Flask](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Portainer Documentation](https://docs.portainer.io/)

---

## 📧 Suporte

Para questões, sugestões ou problemas:
- Abra uma [Issue](https://github.com/josemaeldon/liturgia/issues)
- Envie um Pull Request
- Entre em contato através do GitHub

---

**Desenvolvido com ❤️ para a comunidade católica**