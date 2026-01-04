# 🐳 Instalação no Portainer - Sistema Liturgia

Guia completo e detalhado para deploy do Sistema Liturgia em produção usando Portainer com Docker Swarm.

---

## 📋 Índice

1. [O que é Portainer?](#-o-que-é-portainer)
2. [Pré-requisitos](#-pré-requisitos)
3. [Visão Geral do Processo](#-visão-geral-do-processo)
4. [Passo a Passo Detalhado](#-passo-a-passo-detalhado)
5. [Configuração Avançada](#-configuração-avançada)
6. [Monitoramento e Manutenção](#-monitoramento-e-manutenção)
7. [Troubleshooting](#-troubleshooting)

---

## 🤔 O que é Portainer?

**Portainer** é uma interface web para gerenciar containers Docker de forma visual e intuitiva. Ele simplifica o deploy e gerenciamento de aplicações containerizadas.

**Por que usar Portainer?**
- ✅ Interface visual amigável (não precisa usar terminal)
- ✅ Gerenciamento fácil de stacks Docker Swarm
- ✅ Monitoramento em tempo real
- ✅ Logs centralizados
- ✅ Atualizações simplificadas

---

## ✅ Pré-requisitos

### Servidor

Você precisa de um servidor com:

- **Sistema Operacional:** Linux (Ubuntu 20.04+ recomendado)
- **CPU:** 2+ cores
- **RAM:** 4GB+ (mínimo 2GB)
- **Disco:** 20GB+ de espaço livre
- **Docker:** Instalado e rodando
- **Docker Swarm:** Inicializado
- **Portainer:** Instalado e acessível

### Rede

- **Domínio:** (Opcional) Ex: `liturgia.example.com`
- **Portas abertas:** 
  - 80 (HTTP)
  - 443 (HTTPS - se usar SSL)
  - 9000 (Portainer - já deve estar configurado)

### Acesso

- Acesso administrativo ao Portainer
- Permissões para criar Stacks

---

## 🎯 Visão Geral do Processo

O deploy consiste em 6 etapas principais:

```
1. Acessar Portainer → 2. Criar Stack → 3. Configurar docker-compose.yml 
    → 4. Ajustar Variáveis → 5. Deploy → 6. Verificar
```

**Tempo estimado:** 15-30 minutos

---

## 📝 Passo a Passo Detalhado

### Passo 1: Acessar o Portainer

1. **Abra seu navegador** e acesse seu Portainer:
   ```
   http://seu-servidor:9000
   ```
   ou
   ```
   https://portainer.seu-dominio.com
   ```

2. **Faça login** com suas credenciais de administrador

3. **Selecione seu Environment** (normalmente "primary" ou "local")

---

### Passo 2: Criar Nova Stack

1. No menu lateral, clique em **"Stacks"**

2. Clique no botão **"+ Add stack"** (canto superior direito)

3. **Nomeie a stack:**
   ```
   Nome: liturgia
   ```
   
   > 💡 **Dica:** Use um nome simples e sem espaços

---

### Passo 3: Configurar o Docker Compose

#### Opção A: Web Editor (Mais Fácil)

1. Selecione a aba **"Web editor"**

2. **Cole** o seguinte conteúdo no editor:

```yaml
version: '3.8'

services:
  app:
    image: ghcr.io/josemaeldon/liturgia:latest
    working_dir: /var/www

    networks:
      - liturgianet

    volumes:
      - storage-data:/var/www/storage
      - cache-data:/var/www/bootstrap/cache

    environment:
      APP_NAME: "Liturgia Católica"
      APP_ENV: production
      APP_DEBUG: "false"
      APP_URL: https://liturgia.seu-dominio.com

      # Database configuration - CHANGE THESE VALUES
      DB_CONNECTION: pgsql
      DB_HOST: postgres
      DB_PORT: 5432
      DB_DATABASE: liturgia_db
      DB_USERNAME: postgres
      DB_PASSWORD: "MUDE_ESTA_SENHA_AQUI_123"  # ⚠️ ALTERAR

      # Redis configuration
      REDIS_HOST: redis
      REDIS_PORT: 6379

      # Flask secret key - CHANGE THIS
      SECRET_KEY: "MUDE_ESTA_CHAVE_SECRETA_ALEATORIA_456"  # ⚠️ ALTERAR
      FLASK_ENV: production
      FLASK_DEBUG: "false"
      UPLOAD_FOLDER: /var/www/storage

    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == manager

      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s

      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        order: start-first

      rollback_config:
        parallelism: 1
        delay: 10s

      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

      labels:
        - traefik.enable=true
        - traefik.docker.network=liturgianet
        - traefik.http.routers.liturgia.rule=Host(`liturgia.seu-dominio.com`)
        - traefik.http.routers.liturgia.entrypoints=websecure
        - traefik.http.routers.liturgia.tls.certresolver=letsencryptresolver
        - traefik.http.services.liturgia.loadbalancer.server.port=80
        - traefik.http.middlewares.liturgia-upload.buffering.maxRequestBodyBytes=104857600
        - traefik.http.routers.liturgia.middlewares=liturgia-upload

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: liturgia_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: "MUDE_ESTA_SENHA_AQUI_123"  # ⚠️ DEVE SER IGUAL À DB_PASSWORD
      PGDATA: /var/lib/postgresql/data/pgdata

    volumes:
      - postgres-data:/var/lib/postgresql/data

    networks:
      - liturgianet

    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager

      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes

    volumes:
      - redis-data:/data

    networks:
      - liturgianet

    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager

      restart_policy:
        condition: on-failure

    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

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
  liturgianet:
    driver: overlay
    attachable: true
```

---

### Passo 4: Ajustar Variáveis Importantes

⚠️ **IMPORTANTE:** Você **DEVE** alterar as seguintes configurações antes de fazer o deploy:

#### 4.1. Senhas do Banco de Dados

Encontre estas duas linhas e mude a senha:

```yaml
# Linha ~28 (serviço app)
DB_PASSWORD: "MUDE_ESTA_SENHA_AQUI_123"

# Linha ~97 (serviço postgres)
POSTGRES_PASSWORD: "MUDE_ESTA_SENHA_AQUI_123"
```

⚠️ **As duas senhas DEVEM ser iguais!**

**Como gerar uma senha segura:**
- Use 16+ caracteres
- Misture letras, números e símbolos
- Exemplo: `Lit@urgi4_DB#2026!Segur@`

#### 4.2. Flask Secret Key

Encontre e mude:

```yaml
SECRET_KEY: "MUDE_ESTA_CHAVE_SECRETA_ALEATORIA_456"
```

**Como gerar uma chave secreta:**

No Linux/Mac (terminal):
```bash
openssl rand -hex 32
```

Ou use uma string aleatória longa (40+ caracteres).

#### 4.3. URL da Aplicação (Opcional)

Se você tem um domínio próprio, altere:

```yaml
APP_URL: https://liturgia.seu-dominio.com

# E também nos labels do Traefik:
- traefik.http.routers.liturgia.rule=Host(`liturgia.seu-dominio.com`)
```

> 💡 **Sem domínio?** Use o IP do servidor: `http://192.168.1.100` (exemplo)

#### 4.4. Recursos (Opcional)

Se seu servidor tiver mais ou menos recursos, ajuste:

```yaml
resources:
  limits:
    cpus: '0.5'      # Ajuste conforme necessário
    memory: 512M     # Ajuste conforme necessário
  reservations:
    cpus: '0.25'
    memory: 256M
```

---

### Passo 5: Fazer o Deploy

1. **Revise suas configurações** (especialmente senhas!)

2. **Role até o fim da página** do Portainer

3. Clique no botão **"Deploy the stack"**

4. Aguarde o processo de deploy iniciar

   Você verá mensagens como:
   ```
   Creating network liturgia_liturgianet
   Creating service liturgia_postgres
   Creating service liturgia_redis
   Creating service liturgia_app
   ```

5. **Aguarde 2-3 minutos** para o sistema inicializar completamente

---

### Passo 6: Verificar o Deploy

#### 6.1. Verificar Status dos Services

1. No Portainer, vá em **"Stacks"** → **"liturgia"**

2. Você verá 3 services:
   - `liturgia_app` - Status: ✅ 2/2 (2 réplicas rodando)
   - `liturgia_postgres` - Status: ✅ 1/1
   - `liturgia_redis` - Status: ✅ 1/1

3. Todos devem estar com status **verde** (running)

#### 6.2. Verificar Logs

1. Clique em **"liturgia_app"**

2. Clique em **"Logs"** no topo

3. Você deve ver mensagens como:
   ```
   Liturgia - Starting Container
   Waiting for PostgreSQL to be ready...
   PostgreSQL is ready!
   Initializing database...
   Database initialized successfully!
   Starting Apache...
   ```

4. Se houver erros, veja a seção [Troubleshooting](#-troubleshooting)

#### 6.3. Acessar a Aplicação

Abra seu navegador e acesse:

**Se configurou domínio:**
```
https://liturgia.seu-dominio.com
```

**Se não tem domínio (use IP do servidor):**
```
http://192.168.1.100
```

Você deve ver a página inicial do Sistema Liturgia! 🎉

---

## ⚙️ Configuração Avançada

### Usando Traefik (Proxy Reverso com SSL)

Se você já tem Traefik configurado no seu Swarm:

1. **Certifique-se que os labels Traefik estão corretos:**

```yaml
labels:
  - traefik.enable=true
  - traefik.docker.network=liturgianet
  - traefik.http.routers.liturgia.rule=Host(`liturgia.seu-dominio.com`)
  - traefik.http.routers.liturgia.entrypoints=websecure
  - traefik.http.routers.liturgia.tls.certresolver=letsencryptresolver
  - traefik.http.services.liturgia.loadbalancer.server.port=80
```

2. **Certifique-se que a network existe:**

```bash
# No servidor, via SSH:
docker network create --driver=overlay --attachable liturgianet
```

3. **Se não usar Traefik,** remova todos os labels Traefik e exponha a porta diretamente:

```yaml
ports:
  - "8080:80"  # Expor na porta 8080
```

---

### Configurar Backup Automático

#### Backup do PostgreSQL

1. Crie um novo service de backup na stack:

```yaml
  backup:
    image: postgres:15-alpine
    command: |
      sh -c "while true; do
        pg_dump -h postgres -U postgres liturgia_db > /backup/liturgia_$$(date +%Y%m%d_%H%M%S).sql
        find /backup -name '*.sql' -mtime +7 -delete
        sleep 86400
      done"
    volumes:
      - backup-data:/backup
    networks:
      - liturgianet
    environment:
      PGPASSWORD: "SUA_SENHA_POSTGRES_AQUI"
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
```

2. Adicione o volume de backup:

```yaml
volumes:
  backup-data:
    driver: local
```

---

### Aumentar Número de Réplicas

Para maior disponibilidade:

```yaml
deploy:
  replicas: 4  # Altere de 2 para 4 (ou mais)
```

> ⚠️ **Atenção:** Mais réplicas = mais recursos necessários

---

### Configurar Email (Opcional)

Se quiser notificações por email, adicione ao environment:

```yaml
environment:
  # ... outras vars ...
  MAIL_DRIVER: smtp
  MAIL_HOST: smtp.gmail.com
  MAIL_PORT: 587
  MAIL_USERNAME: seu-email@gmail.com
  MAIL_PASSWORD: sua-senha-app
  MAIL_ENCRYPTION: tls
  MAIL_FROM_ADDRESS: noreply@liturgia.com
  MAIL_FROM_NAME: "Liturgia Católica"
```

---

## 📊 Monitoramento e Manutenção

### Ver Logs em Tempo Real

No Portainer:
1. Vá em **Stacks** → **liturgia**
2. Clique no service (ex: `liturgia_app`)
3. Clique em **Logs**
4. Marque **"Auto-refresh logs"**

### Verificar Health Status

```bash
# Via SSH no servidor
docker service ps liturgia_app
docker service ps liturgia_postgres
docker service ps liturgia_redis
```

Status deve ser **"Running"** para todos.

### Verificar Uso de Recursos

No Portainer:
1. Vá em **Stacks** → **liturgia**
2. Veja o gráfico de CPU e Memória

### Estatísticas Detalhadas

```bash
# Via SSH
docker stats $(docker ps -q --filter "name=liturgia")
```

---

## 🔄 Atualizar a Aplicação

Quando houver uma nova versão:

### Método 1: Via Portainer (Mais Fácil)

1. Vá em **Stacks** → **liturgia**
2. Clique em **"Editor"**
3. Clique em **"Pull and redeploy"** (ícone de atualização)
4. Confirme a ação

O Portainer irá:
- Baixar a imagem mais recente
- Fazer rolling update (zero downtime)
- Manter os dados

### Método 2: Via SSH

```bash
# 1. Atualizar imagem
docker service update --image ghcr.io/josemaeldon/liturgia:latest liturgia_app

# 2. Verificar atualização
docker service ps liturgia_app
```

---

## 🐛 Troubleshooting

### Problema: Services não sobem

**Sintoma:** Status dos services fica em "Starting" ou falha

**Verificar:**

1. **Logs do service:**
   - Portainer → Stacks → liturgia → [service] → Logs

2. **Via SSH:**
```bash
docker service logs liturgia_app
docker service logs liturgia_postgres
```

**Causas comuns:**
- PostgreSQL ainda inicializando (aguarde 2-3 min)
- Senhas incorretas
- Falta de recursos (memória)
- Network não criada

---

### Problema: Erro de conexão com banco de dados

**Erro nos logs:**
```
psycopg2.OperationalError: could not connect to server
```

**Soluções:**

1. **Verificar se PostgreSQL está rodando:**
```bash
docker service ps liturgia_postgres
```

2. **Verificar logs do PostgreSQL:**
```bash
docker service logs liturgia_postgres
```

3. **Verificar senhas:**
   - `DB_PASSWORD` deve ser igual a `POSTGRES_PASSWORD`

4. **Verificar network:**
```bash
docker network ls | grep liturgianet
```

---

### Problema: 502 Bad Gateway

**Sintoma:** Ao acessar a URL, aparece erro 502

**Causas:**
- App ainda está inicializando (aguarde)
- App crashou (veja logs)
- Traefik mal configurado

**Verificar:**

1. **Status do app:**
```bash
docker service ps liturgia_app
```

2. **Logs do app:**
```bash
docker service logs liturgia_app --tail 100
```

3. **Health check:**
```bash
docker service inspect liturgia_app | grep -A 5 Healthcheck
```

---

### Problema: Página não carrega (sem Traefik)

**Se não estiver usando Traefik:**

1. **Expor a porta diretamente:**

Edite a stack e adicione em `app`:
```yaml
ports:
  - "8080:80"
```

2. **Acesse via porta:**
```
http://seu-servidor:8080
```

---

### Problema: Disco cheio

**Verificar espaço:**
```bash
df -h
docker system df
```

**Limpar:**
```bash
# Limpar containers antigos
docker system prune -a

# Limpar volumes não usados (CUIDADO!)
docker volume prune
```

---

### Problema: App reiniciando constantemente

**Verificar:**
```bash
docker service ps liturgia_app --no-trunc
```

**Causas comuns:**
- Erro no código (veja logs)
- Falta de memória
- Health check falhando

**Solução temporária (desabilitar health check):**

Comente/remova o bloco `healthcheck` da stack e faça redeploy.

---

## 📋 Checklist de Deploy

Use este checklist ao fazer o deploy:

- [ ] Portainer acessível e funcionando
- [ ] Docker Swarm inicializado
- [ ] Senha do banco de dados alterada (2 lugares)
- [ ] Secret key do Flask alterada
- [ ] URL da aplicação configurada (se tiver domínio)
- [ ] Network criada (se usar Traefik)
- [ ] Stack criada no Portainer
- [ ] Deploy realizado com sucesso
- [ ] Aguardou 2-3 minutos para inicialização
- [ ] Logs verificados (sem erros)
- [ ] PostgreSQL rodando e saudável
- [ ] Redis rodando e saudável
- [ ] App rodando (2/2 réplicas)
- [ ] Aplicação acessível via navegador
- [ ] Página inicial carregando corretamente
- [ ] Testado criar uma missa personalizada
- [ ] Testado consultar liturgia do dia

---

## 🎓 Recursos Adicionais

### Documentação Relacionada

- 📖 [README Principal](README.md)
- 📦 [Instalação Local](INSTALL_LOCAL.md)
- 🔧 [Guia de Uso](USAGE.md)
- 🐋 [Docker Deployment](DOCKER_DEPLOYMENT.md)

### Ferramentas Úteis

- [Portainer Documentation](https://docs.portainer.io/)
- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)

### Comandos Úteis Docker Swarm

```bash
# Listar stacks
docker stack ls

# Listar services de uma stack
docker stack services liturgia

# Ver detalhes de um service
docker service inspect liturgia_app

# Escalar service
docker service scale liturgia_app=4

# Remover stack
docker stack rm liturgia

# Ver todos os containers
docker ps
```

---

## 🆘 Precisa de Ajuda?

- 🐛 [Abrir Issue no GitHub](https://github.com/josemaeldon/liturgia/issues)
- 📖 [Consultar Documentação](README.md)
- 💬 Verificar logs no Portainer

---

## 🎉 Conclusão

Parabéns! Você deployou com sucesso o Sistema Liturgia em produção usando Portainer!

**Próximos passos:**
- 📖 Leia o [Guia de Uso](USAGE.md) para explorar todas as funcionalidades
- 🔐 Configure SSL/HTTPS com Let's Encrypt
- 📊 Configure backups automáticos
- 🔔 Configure monitoramento e alertas

**Deploy bem-sucedido! 🚀**
