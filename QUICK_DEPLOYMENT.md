# Quick Deployment Reference

Este guia resume as opções de deployment disponíveis para o sistema Liturgia.

## 🚀 Stack Recomendada para Produção

### PostgreSQL + Apache + Docker Swarm

**📖 Guia completo:** [POSTGRES_APACHE_DEPLOYMENT.md](POSTGRES_APACHE_DEPLOYMENT.md)

```bash
# Deploy rápido
cp .env.example .env
# Editar .env com suas configurações
docker stack deploy -c docker-compose.yml liturgia
```

**Stack inclui:**
- ✅ Apache com mod_wsgi (porta 80)
- ✅ PostgreSQL 15 (banco de dados)
- ✅ Redis 7 (cache)
- ✅ Traefik (SSL automático)
- ✅ Volumes persistentes
- ✅ Health checks
- ✅ Auto-scaling

**Ideal para:**
- Produção com múltiplas réplicas
- Ambientes com Traefik
- Alta disponibilidade
- Integração com stacks existentes

## 📚 Outras Opções de Deployment

### 1. Gunicorn + Nginx

**📖 Guia completo:** [DEPLOYMENT.md](DEPLOYMENT.md)

Deployment tradicional com Gunicorn como servidor WSGI e Nginx como reverse proxy.

**Ideal para:**
- Servidores VPS tradicionais
- Deploy sem Docker
- Ambientes com Nginx existente

### 2. Docker Básico

**📖 Guia completo:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

Deployment Docker simples com Gunicorn (configuração anterior).

**Ideal para:**
- Desenvolvimento
- Testes
- Deploy simples sem PostgreSQL

## 🔄 Comparação

| Recurso | Apache Stack | Gunicorn+Nginx | Docker Básico |
|---------|-------------|----------------|---------------|
| Servidor Web | Apache | Gunicorn+Nginx | Gunicorn |
| Banco de Dados | PostgreSQL | Configurável | Nenhum |
| Cache | Redis | Opcional | Nenhum |
| SSL Automático | ✅ Traefik | Manual | Manual |
| Docker Swarm | ✅ | ❌ | Parcial |
| Alta Disponibilidade | ✅ | Manual | ❌ |
| Auto-scaling | ✅ | ❌ | ❌ |
| Complexidade | Média | Baixa | Muito Baixa |

## 🎯 Escolha Rápida

**Use Apache Stack se:**
- ✅ Já tem infraestrutura Docker Swarm
- ✅ Precisa de banco de dados persistente
- ✅ Quer SSL automático com Traefik
- ✅ Precisa escalar horizontalmente

**Use Gunicorn+Nginx se:**
- ✅ Tem servidor VPS tradicional
- ✅ Não quer usar Docker
- ✅ Já tem Nginx configurado

**Use Docker Básico se:**
- ✅ Apenas desenvolvimento/testes
- ✅ Quer algo simples e rápido
- ✅ Não precisa de persistência

## 📋 Checklist Pré-Deploy

Antes de fazer deploy em produção:

- [ ] Escolher stack adequada
- [ ] Configurar variáveis de ambiente (.env)
- [ ] Gerar SECRET_KEY forte
- [ ] Configurar senhas do banco de dados
- [ ] Configurar domínio e DNS
- [ ] Configurar SSL/TLS
- [ ] Configurar backups
- [ ] Testar health checks
- [ ] Configurar monitoramento
- [ ] Documentar credenciais (em local seguro)

## 🔐 Segurança

**Sempre em produção:**

```bash
# Gerar SECRET_KEY
openssl rand -hex 32

# Gerar senha do PostgreSQL
openssl rand -hex 16

# Configurar no .env
SECRET_KEY=<chave-gerada>
DB_PASSWORD=<senha-gerada>
APP_DEBUG=false
```

## 📞 Suporte

- **Issues:** https://github.com/josemaeldon/liturgia/issues
- **Documentação:** README.md
- **Deployment:** POSTGRES_APACHE_DEPLOYMENT.md

## 🚀 Deploy em 5 Minutos

```bash
# 1. Clone o repositório
git clone https://github.com/josemaeldon/liturgia.git
cd liturgia

# 2. Configure ambiente
cp .env.example .env
nano .env  # Editar SECRET_KEY e DB_PASSWORD

# 3. Deploy
docker stack deploy -c docker-compose.yml liturgia

# 4. Verificar
docker stack services liturgia

# 5. Acessar
# https://seu-dominio.com
```

## 📊 Monitoramento Rápido

```bash
# Status dos serviços
docker service ls

# Logs da aplicação
docker service logs -f liturgia_app

# Logs do PostgreSQL
docker service logs -f liturgia_postgres

# Recursos
docker stats
```

## 🔄 Manutenção Rápida

```bash
# Atualizar aplicação
docker service update --image ghcr.io/josemaeldon/liturgia:latest liturgia_app

# Escalar réplicas
docker service scale liturgia_app=3

# Backup do banco
docker exec $(docker ps -q --filter "name=liturgia_postgres") \
  pg_dump -U postgres liturgia_db > backup.sql

# Rollback
docker service rollback liturgia_app
```

## 📖 Leitura Adicional

- [README.md](README.md) - Visão geral do projeto
- [USAGE.md](USAGE.md) - Como usar o sistema
- [WEB_README.md](WEB_README.md) - Interface web
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy com Gunicorn/Nginx
- [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) - Deploy Docker básico
- [POSTGRES_APACHE_DEPLOYMENT.md](POSTGRES_APACHE_DEPLOYMENT.md) - Deploy completo
