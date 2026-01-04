# 📚 Índice da Documentação - Sistema Liturgia

Guia completo de toda a documentação disponível do Sistema Liturgia.

---

## 🚀 Início Rápido

Novo no sistema? Comece aqui:

1. 📖 **[README.md](README.md)** - Visão geral do projeto e introdução
2. 📦 **[INSTALL_LOCAL.md](INSTALL_LOCAL.md)** - Instalação local (desenvolvimento)
3. 🐳 **[INSTALL_PORTAINER.md](INSTALL_PORTAINER.md)** - Instalação no Portainer (produção)

---

## 📖 Documentação Principal

### Para Usuários

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **[README.md](README.md)** | Visão geral do sistema, características e links principais | Primeira leitura |
| **[USAGE.md](USAGE.md)** | Guia de uso da aplicação e API Python | Aprender a usar o sistema |
| **[WEB_README.md](WEB_README.md)** | Interface web e funcionalidades | Usar a interface web |

### Para Desenvolvedores

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| **[INSTALL_LOCAL.md](INSTALL_LOCAL.md)** | Instalação local detalhada | Desenvolvimento local |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Arquitetura do sistema | Entender a estrutura |
| **[DATABASE_INTEGRATION.md](DATABASE_INTEGRATION.md)** | Integração com PostgreSQL | Trabalhar com banco de dados |

---

## 🐳 Guias de Deploy

### Deploy Recomendado (Portainer)

**🎯 Para produção com interface visual**

1. **[INSTALL_PORTAINER.md](INSTALL_PORTAINER.md)** ⭐ **RECOMENDADO**
   - Guia completo passo a passo
   - Deploy via interface Portainer
   - Ideal para produção
   - Inclui troubleshooting

### Outras Opções de Deploy

| Documento | Descrição | Ideal Para |
|-----------|-----------|------------|
| **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** | Deploy com Docker Compose/Swarm | Deploy rápido com Docker CLI |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Deploy manual (Gunicorn, Nginx, Systemd) | Servidores tradicionais sem Docker |
| **[POSTGRES_APACHE_DEPLOYMENT.md](POSTGRES_APACHE_DEPLOYMENT.md)** | Stack completa PostgreSQL + Apache | Referência técnica detalhada |

---

## 🔧 Documentação Técnica

### Arquitetura e Design

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura geral do sistema
- **[DATABASE_INTEGRATION.md](DATABASE_INTEGRATION.md)** - Modelos de dados e PostgreSQL

### Configuração

- **[.env.example](.env.example)** - Exemplo de variáveis de ambiente
- **[docker-compose.yml](docker-compose.yml)** - Configuração Docker Swarm/Compose
- **[requirements.txt](requirements.txt)** - Dependências Python

---

## 📂 Estrutura da Documentação

```
liturgia/
├── README.md                          # 📖 Visão geral
├── DOCS_INDEX.md                      # 📚 Este índice
│
├── Instalação e Setup
│   ├── INSTALL_LOCAL.md              # 📦 Instalação local
│   └── INSTALL_PORTAINER.md          # 🐳 Instalação Portainer
│
├── Uso e Funcionalidades
│   ├── USAGE.md                      # 📖 Guia de uso
│   └── WEB_README.md                 # 🌐 Interface web
│
├── Deploy e Produção
│   ├── DOCKER_DEPLOYMENT.md          # 🐋 Deploy Docker
│   ├── DEPLOYMENT.md                 # 📘 Deploy manual
│   └── POSTGRES_APACHE_DEPLOYMENT.md # 🗄️ Stack completa
│
└── Documentação Técnica
    ├── ARCHITECTURE.md               # 🏗️ Arquitetura
    └── DATABASE_INTEGRATION.md       # 🗄️ Banco de dados
```

---

## 🎯 Escolher a Documentação Certa

### Quero instalar localmente para desenvolvimento
👉 **[INSTALL_LOCAL.md](INSTALL_LOCAL.md)**

### Quero fazer deploy em produção com Portainer
👉 **[INSTALL_PORTAINER.md](INSTALL_PORTAINER.md)**

### Quero fazer deploy em produção sem Portainer
👉 **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** ou **[DEPLOYMENT.md](DEPLOYMENT.md)**

### Quero aprender a usar o sistema
👉 **[USAGE.md](USAGE.md)** e **[WEB_README.md](WEB_README.md)**

### Quero entender a arquitetura
👉 **[ARCHITECTURE.md](ARCHITECTURE.md)**

### Quero trabalhar com o banco de dados
👉 **[DATABASE_INTEGRATION.md](DATABASE_INTEGRATION.md)**

---

## 📝 Fluxo de Leitura Recomendado

### Para Novos Usuários

```
1. README.md (visão geral)
   ↓
2. INSTALL_LOCAL.md (instalação)
   ↓
3. USAGE.md (como usar)
   ↓
4. Explorar exemplos em /examples
```

### Para Deploy em Produção

```
1. README.md (visão geral)
   ↓
2. INSTALL_PORTAINER.md (passo a passo completo)
   ↓
3. Configurar variáveis de ambiente
   ↓
4. Deploy e monitoramento
```

### Para Desenvolvedores

```
1. README.md (visão geral)
   ↓
2. INSTALL_LOCAL.md (setup local)
   ↓
3. ARCHITECTURE.md (entender estrutura)
   ↓
4. DATABASE_INTEGRATION.md (banco de dados)
   ↓
5. Código fonte em /models, /templates, etc.
```

---

## 🔍 Referência Rápida

### Comandos Importantes

**Local Development:**
```bash
python app.py                           # Executar localmente
python examples/example_epifania.py     # Executar exemplo
```

**Docker:**
```bash
docker-compose up -d                    # Docker Compose
docker stack deploy -c docker-compose.yml liturgia  # Docker Swarm
```

**Portainer:**
- Acesse via interface web
- Crie Stack com docker-compose.yml
- Configure variáveis de ambiente

### Arquivos de Configuração

| Arquivo | Propósito |
|---------|-----------|
| `.env.example` | Exemplo de variáveis de ambiente |
| `docker-compose.yml` | Orquestração Docker |
| `requirements.txt` | Dependências Python |
| `Dockerfile` | Imagem Docker |

---

## 🆘 Precisa de Ajuda?

### Por Tópico

- **Instalação Local:** [INSTALL_LOCAL.md](INSTALL_LOCAL.md) → Seção Troubleshooting
- **Deploy Portainer:** [INSTALL_PORTAINER.md](INSTALL_PORTAINER.md) → Seção Troubleshooting
- **Uso da Aplicação:** [USAGE.md](USAGE.md)
- **Problemas com Banco:** [DATABASE_INTEGRATION.md](DATABASE_INTEGRATION.md)

### Suporte Geral

- 🐛 **Issues:** [GitHub Issues](https://github.com/josemaeldon/liturgia/issues)
- 📖 **Documentação:** Este índice e documentos relacionados
- 💬 **Discussões:** [GitHub Discussions](https://github.com/josemaeldon/liturgia/discussions)

---

## 📊 Status dos Documentos

| Documento | Status | Última Atualização |
|-----------|--------|-------------------|
| README.md | ✅ Atualizado | 2026-01-04 |
| INSTALL_LOCAL.md | ✅ Novo | 2026-01-04 |
| INSTALL_PORTAINER.md | ✅ Novo | 2026-01-04 |
| ARCHITECTURE.md | ✅ Novo | 2026-01-04 |
| USAGE.md | ✅ Atualizado | 2025 |
| WEB_README.md | ✅ Atualizado | 2025 |
| DATABASE_INTEGRATION.md | ✅ Atualizado | 2025 |
| DOCKER_DEPLOYMENT.md | ✅ Mantido | 2025 |
| DEPLOYMENT.md | ✅ Mantido | 2025 |
| POSTGRES_APACHE_DEPLOYMENT.md | ✅ Mantido | 2025 |

---

## 🔄 Mantendo a Documentação Atualizada

Se você fizer alterações significativas no projeto:

1. ✅ Atualize o documento relevante
2. ✅ Atualize este índice se necessário
3. ✅ Verifique links internos
4. ✅ Atualize a data de "Última Atualização"

---

## 📚 Documentos Legados/Arquivados

Os seguintes documentos são relatórios/resumos de implementações anteriores e podem ser arquivados:

- `IMPLEMENTATION_SUMMARY.md` - Resumo de implementação
- `SUMMARY.md` - Resumo do sistema
- `VERIFICATION_REPORT.md` - Relatório de verificação
- `QUICK_DEPLOYMENT.md` - Referência rápida (integrada ao README)

Estes documentos estão disponíveis no repositório mas não são necessários para uso diário.

---

## 🎓 Recursos Adicionais

### Exemplos Práticos

Explore os exemplos na pasta `examples/`:
- `example_epifania.py` - Missa completa
- `example_daily_liturgy.py` - Liturgia diária
- `example_liturgy_hours.py` - Liturgia das horas
- `example_all_hours.py` - Todas as 7 horas
- `example_custom_mass.py` - Missa personalizada

### Links Externos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Portainer Documentation](https://docs.portainer.io/)

---

**Última atualização:** 2026-01-04
**Versão:** 2.0
**Mantido por:** Projeto Liturgia
