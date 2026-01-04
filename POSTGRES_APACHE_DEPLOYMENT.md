# Deployment Guide - PostgreSQL + Apache Stack

Este guia explica como fazer o deploy do sistema Liturgia usando PostgreSQL e Apache em um ambiente Docker Swarm, similar à stack do Fluxo de Caixa.

## 📋 Índice

1. [Visão Geral da Stack](#visão-geral-da-stack)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração](#configuração)
4. [Deploy no Docker Swarm](#deploy-no-docker-swarm)
5. [Variáveis de Ambiente](#variáveis-de-ambiente)
6. [Integração com Traefik](#integração-com-traefik)
7. [Backup e Manutenção](#backup-e-manutenção)
8. [Troubleshooting](#troubleshooting)

## 🏗️ Visão Geral da Stack

A stack de produção consiste em:

- **App (Apache + mod_wsgi)**: Aplicação Flask rodando no Apache
- **PostgreSQL**: Banco de dados para armazenamento persistente
- **Redis**: Cache e sessões (opcional)
- **Traefik**: Reverse proxy com SSL automático

### Arquitetura

```
┌─────────────┐
│   Traefik   │  ← HTTPS (443)
│  (SSL/TLS)  │
└──────┬──────┘
       │
       ├──────────┐
       │          │
┌──────▼──────┐   │
│  Liturgia   │   │
│   Apache    │◄──┘
│  (Port 80)  │
└──────┬──────┘
       │
   ┌───┴────┬──────┐
   │        │      │
┌──▼───┐ ┌─▼──┐ ┌─▼────┐
│Postgres│ │Redis│ │Volume│
└────────┘ └────┘ └──────┘
```

## 🔧 Pré-requisitos

### Infraestrutura

- Docker Engine 20.10+
- Docker Swarm inicializado
- Acesso ao nó manager do Swarm
- Traefik configurado (para SSL automático)

### Rede

- Porta 80 (HTTP) - Comunicação interna
- Porta 443 (HTTPS) - Traefik
- Rede overlay `liturgianet` ou externa (`luzianet` no exemplo)

### Recursos Mínimos

Por réplica da aplicação:
- **CPU**: 0.25 cores (mínimo), 0.5 cores (limite)
- **RAM**: 256 MB (mínimo), 512 MB (limite)

PostgreSQL:
- **CPU**: 0.5 cores
- **RAM**: 512 MB
- **Disco**: 5 GB (inicial)

### ⚠️ Considerações Importantes

**Placement Constraints:**
- A configuração padrão coloca todos os serviços em nós manager (`node.role == manager`)
- Isso segue o padrão do Fluxo de Caixa e funciona bem para clusters pequenos
- Para ambientes multi-node maiores, considere:
  - Remover a constraint da aplicação para permitir deploy em workers
  - Manter apenas PostgreSQL e Redis em managers para garantir persistência
  - Usar volumes compartilhados (NFS, GlusterFS) para dados persistentes

**Volumes:**
- A configuração usa `driver: local` para volumes
- Adequado para single-node ou manager-only deployments
- Para clusters multi-node, considere:
  - Usar driver de storage compartilhado (NFS, GlusterFS, Ceph)
  - Ou volumes externos gerenciados pela infraestrutura
  - Garantir que volumes de dados estejam sempre disponíveis

**Escalabilidade:**
- Com 2 réplicas padrão, suporta ~40-80 req/s
- Para aumentar capacidade, escalar réplicas: `docker service scale liturgia_app=5`
- PostgreSQL não escala horizontalmente (usar read replicas se necessário)

## ⚙️ Configuração

### 1. Preparar Variáveis de Ambiente

Crie um arquivo `.env` no diretório do projeto:

```bash
# Arquivo: .env

# Aplicação
APP_NAME="Liturgia Católica"
APP_ENV=production
APP_DEBUG=false
APP_URL=https://liturgia.santaluzia.org

# Flask Secret Key (gere uma chave segura)
SECRET_KEY=$(openssl rand -hex 32)

# Banco de Dados PostgreSQL
DB_CONNECTION=pgsql
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=liturgia_db
DB_USERNAME=postgres
DB_PASSWORD=$(openssl rand -hex 16)

# Redis (opcional)
REDIS_HOST=redis
REDIS_PORT=6379

# Storage/Upload
UPLOAD_FOLDER=/var/www/storage
```

**⚠️ IMPORTANTE**: Gere senhas fortes para produção:

```bash
# Gerar SECRET_KEY
openssl rand -hex 32

# Gerar DB_PASSWORD
openssl rand -hex 16
```

### 2. Criar o Stack File

Edite o `docker-compose.yml` com suas configurações:

```yaml
version: '3.8'

services:
  app:
    image: ghcr.io/josemaeldon/liturgia:latest
    working_dir: /var/www

    networks:
      - luzianet  # Use sua rede existente

    volumes:
      - storage-data:/var/www/storage
      - cache-data:/var/www/bootstrap/cache

    environment:
      APP_NAME: "Liturgia Católica"
      APP_ENV: production
      APP_DEBUG: "false"
      APP_URL: https://liturgia.santaluzia.org

      DB_CONNECTION: pgsql
      DB_HOST: postgres
      DB_PORT: 5432
      DB_DATABASE: liturgia_db
      DB_USERNAME: postgres
      DB_PASSWORD: ${DB_PASSWORD}

      REDIS_HOST: redis
      REDIS_PORT: 6379

      SECRET_KEY: ${SECRET_KEY}
      FLASK_ENV: production
      UPLOAD_FOLDER: /var/www/storage

    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == manager

      labels:
        - traefik.enable=true
        - traefik.docker.network=luzianet

        - traefik.http.routers.liturgia.rule=Host(`liturgia.santaluzia.org`)
        - traefik.http.routers.liturgia.entrypoints=websecure
        - traefik.http.routers.liturgia.tls.certresolver=letsencryptresolver
        - traefik.http.services.liturgia.loadbalancer.server.port=80

        # Aumentar limite de upload (100MB)
        - traefik.http.middlewares.liturgia-upload.buffering.maxRequestBodyBytes=104857600
        - traefik.http.middlewares.liturgia-upload.buffering.memRequestBodyBytes=2097152
        - traefik.http.routers.liturgia.middlewares=liturgia-upload

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: liturgia_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata

    volumes:
      - postgres-data:/var/lib/postgresql/data

    networks:
      - luzianet

    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes

    volumes:
      - redis-data:/data

    networks:
      - luzianet

    deploy:
      replicas: 1

volumes:
  cache-data:
    driver: local
  storage-data:
    driver: local
  postgres-data:
    driver: local
  redis-data:
    driver: local

networks:
  luzianet:
    external: true
```

### 3. Configurar Rede Externa

Se estiver usando uma rede existente (como `luzianet`):

```bash
# Verificar se a rede existe
docker network ls | grep luzianet

# Se não existir, criar
docker network create --driver overlay --attachable luzianet
```

## 🚀 Deploy no Docker Swarm

### 1. Deploy da Stack

```bash
# Fazer deploy da stack completa
docker stack deploy -c docker-compose.yml liturgia

# Verificar serviços
docker stack services liturgia

# Verificar status detalhado
docker service ps liturgia_app
docker service ps liturgia_postgres
docker service ps liturgia_redis
```

### 2. Verificar Logs

```bash
# Logs da aplicação
docker service logs -f liturgia_app

# Logs do PostgreSQL
docker service logs -f liturgia_postgres

# Logs do Redis
docker service logs -f liturgia_redis

# Últimas 100 linhas
docker service logs --tail 100 liturgia_app
```

### 3. Inicializar Banco de Dados

Se sua aplicação precisar de migrations ou inicialização:

```bash
# Conectar a um container da aplicação
CONTAINER_ID=$(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_app" | head -1)
docker exec -it $CONTAINER_ID bash

# Dentro do container, executar migrations
python manage.py db upgrade  # Se usar Flask-Migrate
# ou
python init_db.py  # Script customizado

# Sair
exit
```

### 4. Acessar PostgreSQL

```bash
# Conectar ao PostgreSQL
POSTGRES_CONTAINER=$(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres")
docker exec -it $POSTGRES_CONTAINER psql -U postgres -d liturgia_db

# Executar queries
liturgia_db=# \dt  # Listar tabelas
liturgia_db=# SELECT * FROM liturgias LIMIT 5;
liturgia_db=# \q  # Sair
```

## 🔐 Variáveis de Ambiente

### Essenciais

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `SECRET_KEY` | Chave secreta do Flask | `abc123...` (32+ chars) |
| `DB_PASSWORD` | Senha do PostgreSQL | `secure_password_123` |
| `APP_URL` | URL da aplicação | `https://liturgia.santaluzia.org` |

### Opcionais

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `APP_NAME` | Nome da aplicação | `Liturgia Católica` |
| `APP_DEBUG` | Modo debug | `false` |
| `DB_HOST` | Host do PostgreSQL | `postgres` |
| `DB_PORT` | Porta do PostgreSQL | `5432` |
| `DB_DATABASE` | Nome do banco | `liturgia_db` |
| `DB_USERNAME` | Usuário do banco | `postgres` |
| `REDIS_HOST` | Host do Redis | `redis` |
| `REDIS_PORT` | Porta do Redis | `6379` |
| `UPLOAD_FOLDER` | Diretório de uploads | `/var/www/storage` |

### Usando Docker Secrets (Recomendado para Produção)

```bash
# Criar secrets
echo "sua-secret-key-super-segura" | docker secret create liturgia_secret_key -
echo "senha-postgresql-segura" | docker secret create liturgia_db_password -

# Atualizar docker-compose.yml para usar secrets
```

No `docker-compose.yml`:

```yaml
services:
  app:
    secrets:
      - liturgia_secret_key
      - liturgia_db_password
    environment:
      SECRET_KEY_FILE: /run/secrets/liturgia_secret_key
      DB_PASSWORD_FILE: /run/secrets/liturgia_db_password

secrets:
  liturgia_secret_key:
    external: true
  liturgia_db_password:
    external: true
```

## 🌐 Integração com Traefik

### Configuração Traefik

A stack já vem configurada com labels do Traefik. Certifique-se de que:

1. **Traefik está rodando** no seu Swarm
2. **Rede está correta** (`luzianet` ou outra)
3. **Cert resolver está configurado** (`letsencryptresolver`)

### Labels do Traefik

```yaml
deploy:
  labels:
    # Habilitar Traefik
    - traefik.enable=true
    - traefik.docker.network=luzianet
    
    # Roteamento
    - traefik.http.routers.liturgia.rule=Host(`liturgia.santaluzia.org`)
    - traefik.http.routers.liturgia.entrypoints=websecure
    
    # SSL/TLS
    - traefik.http.routers.liturgia.tls=true
    - traefik.http.routers.liturgia.tls.certresolver=letsencryptresolver
    
    # Porta do serviço
    - traefik.http.services.liturgia.loadbalancer.server.port=80
    
    # Middleware para upload de arquivos grandes
    - traefik.http.middlewares.liturgia-upload.buffering.maxRequestBodyBytes=104857600
    - traefik.http.routers.liturgia.middlewares=liturgia-upload
```

### Testar Acesso

```bash
# Testar HTTP
curl http://liturgia.santaluzia.org

# Testar HTTPS
curl https://liturgia.santaluzia.org

# Ver certificado SSL
openssl s_client -connect liturgia.santaluzia.org:443 -servername liturgia.santaluzia.org
```

## 🔄 Atualização e Manutenção

### Atualizar Aplicação

```bash
# Fazer pull da nova imagem
docker pull ghcr.io/josemaeldon/liturgia:latest

# Atualizar serviço (rolling update)
docker service update --image ghcr.io/josemaeldon/liturgia:latest liturgia_app

# Ou re-deploy da stack completa
docker stack deploy -c docker-compose.yml liturgia
```

### Escalar Réplicas

```bash
# Aumentar para 3 réplicas
docker service scale liturgia_app=3

# Reduzir para 1 réplica
docker service scale liturgia_app=1
```

### Rollback

```bash
# Voltar para versão anterior
docker service rollback liturgia_app

# Ver histórico de updates
docker service ps liturgia_app
```

## 💾 Backup e Restore

### Backup do PostgreSQL

```bash
# Criar backup
docker exec $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres") \
  pg_dump -U postgres liturgia_db > backup_$(date +%Y%m%d).sql

# Backup comprimido
docker exec $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres") \
  pg_dump -U postgres liturgia_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore do PostgreSQL

```bash
# Restaurar backup
cat backup_20240115.sql | docker exec -i $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres") \
  psql -U postgres liturgia_db

# Restaurar backup comprimido
gunzip < backup_20240115.sql.gz | docker exec -i $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres") \
  psql -U postgres liturgia_db
```

### Backup dos Volumes

```bash
# Backup do volume de storage
docker run --rm \
  -v liturgia_storage-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/storage_backup_$(date +%Y%m%d).tar.gz /data

# Backup do volume do PostgreSQL
docker run --rm \
  -v liturgia_postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup_$(date +%Y%m%d).tar.gz /data
```

### Script de Backup Automático

Crie um script `/usr/local/bin/backup-liturgia.sh`:

```bash
#!/bin/bash
# Backup automático da stack Liturgia

BACKUP_DIR="/backups/liturgia"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
echo "Backing up PostgreSQL..."
docker exec $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres") \
  pg_dump -U postgres liturgia_db | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Backup volumes
echo "Backing up volumes..."
docker run --rm \
  -v liturgia_storage-data:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/storage_$DATE.tar.gz /data

# Remover backups antigos (manter últimos 7 dias)
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR"
```

Tornar executável e agendar no cron:

```bash
chmod +x /usr/local/bin/backup-liturgia.sh

# Adicionar ao crontab (backup diário às 2h da manhã)
crontab -e
# Adicionar linha:
0 2 * * * /usr/local/bin/backup-liturgia.sh >> /var/log/backup-liturgia.log 2>&1
```

## 🔍 Monitoramento

### Health Checks

```bash
# Status dos serviços
docker service ls

# Health check da aplicação
curl http://liturgia.santaluzia.org/health

# Status do PostgreSQL
docker exec $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres") \
  pg_isready -U postgres

# Status do Redis
docker exec $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_redis") \
  redis-cli ping
```

### Logs e Debugging

```bash
# Logs em tempo real
docker service logs -f liturgia_app

# Logs com timestamp
docker service logs --timestamps liturgia_app

# Últimas 100 linhas
docker service logs --tail 100 liturgia_app

# Logs de todas as réplicas
docker service ps liturgia_app --no-trunc
```

### Recursos e Performance

```bash
# Uso de CPU e memória
docker stats

# Stats de um serviço específico
docker stats $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_app")

# Espaço em disco dos volumes
docker system df -v
```

## 🐛 Troubleshooting

### Serviço não inicia

```bash
# Verificar logs
docker service logs liturgia_app

# Verificar eventos
docker events --filter service=liturgia_app

# Inspecionar serviço
docker service inspect liturgia_app

# Verificar tarefas com erro
docker service ps liturgia_app --no-trunc
```

### Erro de conexão com PostgreSQL

```bash
# Verificar se PostgreSQL está rodando
docker service ps liturgia_postgres

# Testar conexão
docker exec -it $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_app" | head -1) \
  nc -zv postgres 5432

# Verificar logs do PostgreSQL
docker service logs liturgia_postgres

# Verificar credenciais
docker service inspect liturgia_app --format '{{json .Spec.TaskTemplate.ContainerSpec.Env}}'
```

### Erro 502 Bad Gateway

```bash
# Verificar se app está respondendo
curl http://localhost/

# Verificar porta no Traefik
docker service inspect liturgia_app | grep -A 5 traefik.http.services

# Verificar logs do Traefik
docker service logs traefik
```

### Volume de disco cheio

```bash
# Ver uso de disco
df -h

# Limpar containers parados
docker system prune -a

# Limpar volumes não utilizados
docker volume prune

# Ver tamanho dos volumes
docker system df -v
```

### Performance lenta

```bash
# Verificar recursos
docker stats

# Aumentar réplicas
docker service scale liturgia_app=3

# Verificar queries lentas no PostgreSQL
docker exec -it $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres") \
  psql -U postgres -d liturgia_db -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
```

## 📊 Configurações de Produção

### Checklist de Segurança

- [ ] SECRET_KEY forte e único
- [ ] Senhas do PostgreSQL seguras
- [ ] APP_DEBUG=false
- [ ] HTTPS habilitado via Traefik
- [ ] Firewall configurado
- [ ] Backups automáticos configurados
- [ ] Monitoramento configurado
- [ ] Logs sendo coletados
- [ ] Rate limiting configurado no Traefik
- [ ] Health checks funcionando

### Otimizações

```yaml
# Aumentar recursos se necessário
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Configuração Apache Avançada

Para ajustes finos do Apache, crie um Dockerfile customizado:

```dockerfile
FROM ghcr.io/josemaeldon/liturgia:latest

# Configuração customizada do Apache
RUN echo 'MaxRequestWorkers 150\n\
    ServerLimit 150\n\
    StartServers 5\n\
    MinSpareServers 5\n\
    MaxSpareServers 10' >> /etc/apache2/apache2.conf
```

## 📚 Referências

- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Apache mod_wsgi](https://modwsgi.readthedocs.io/)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)

## 📞 Suporte

Para problemas ou dúvidas:
- GitHub Issues: https://github.com/josemaeldon/liturgia/issues
- Documentação: README.md e outros guias

## 📄 Licença

MIT License - Veja o arquivo LICENSE para detalhes.
