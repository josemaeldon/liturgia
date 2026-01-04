# Database Integration Guide

Este documento explica como funciona a integração com PostgreSQL no sistema Liturgia.

## 📦 Arquitetura do Banco de Dados

### Modelos de Dados

O sistema usa **SQLAlchemy** como ORM e contém os seguintes modelos:

#### 1. **LiturgicalColor** (Cores Litúrgicas)
```python
- id: Integer (PK)
- name: String (verde, branco, vermelho, roxo, rosa)
- meaning: Text
```

#### 2. **Celebration** (Celebrações)
```python
- id: Integer (PK)
- name: String
- date: Date (indexed)
- type: String (solenidade, festa, memória, feria)
- season: String (tempo comum, advento, natal, quaresma, páscoa)
- color_id: Foreign Key → LiturgicalColor
```

#### 3. **Reading** (Leituras Bíblicas)
```python
- id: Integer (PK)
- reference: String (ex: "Mt 2,1-12")
- text: Text
- book: String
- chapter: Integer
- verses: String
- created_at: DateTime
```

#### 4. **Psalm** (Salmos Responsoriais)
```python
- id: Integer (PK)
- number: Integer
- reference: String
- response: Text
- verses: Text
- created_at: DateTime
```

#### 5. **Prayer** (Orações Litúrgicas)
```python
- id: Integer (PK)
- title: String
- text: Text
- response: Text
- category: String (collect, offertory, communion)
- created_at: DateTime
```

#### 6. **DailyLiturgy** (Liturgia Diária)
```python
- id: Integer (PK)
- celebration_id: FK → Celebration
- first_reading_id: FK → Reading
- psalm_id: FK → Psalm
- second_reading_id: FK → Reading
- gospel_id: FK → Reading
- collect_prayer_id: FK → Prayer
- offertory_prayer_id: FK → Prayer
- communion_prayer_id: FK → Prayer
- created_at, updated_at: DateTime
```

#### 7. **Antiphon** (Antífonas)
```python
- id: Integer (PK)
- type: String (entrance, communion, offertory)
- text: Text
- reference: String
- celebration_id: FK → Celebration
- created_at: DateTime
```

#### 8. **LiturgyHour** (Liturgia das Horas)
```python
- id: Integer (PK)
- date: Date (indexed)
- hour_type: String (office_readings, laudes, terca, sexta, nona, vesperas, completas)
- content: JSON
- created_at, updated_at: DateTime
- UNIQUE(date, hour_type)
```

#### 9. **CustomMass** (Missas Personalizadas)
```python
- id: Integer (PK)
- name: String
- celebration_name: String
- celebration_date: Date
- celebration_color: String
- entrance_antiphon: Text
- communion_antiphon: Text
- custom_prayers: JSON
- readings: JSON
- created_at, updated_at: DateTime
- created_by: String
```

## 🚀 Inicialização Automática

### Como Funciona

Quando o container Docker inicia, o script `entrypoint.sh` executa:

1. **Aguarda PostgreSQL** (até 30 tentativas, 2 segundos cada)
2. **Executa init_db.py** que:
   - Cria todas as tabelas (`db.create_all()`)
   - Insere dados iniciais (cores litúrgicas, celebrações exemplo, etc.)
3. **Inicia Apache** em foreground

### Dados Iniciais Carregados

O `init_db.py` carrega:

- ✅ 5 Cores Litúrgicas (verde, branco, vermelho, roxo, rosa)
- ✅ 3 Celebrações de exemplo (Epifania, Domingo Ordinário, Pentecostes)
- ✅ 3 Leituras bíblicas de exemplo
- ✅ 2 Salmos responsoriais
- ✅ 2 Orações litúrgicas
- ✅ 1 Liturgia diária completa (Epifania)

### Verificação

Após inicialização, o banco contém:
```
Liturgical Colors: 5
Celebrations: 3
Readings: 3
Psalms: 2
Prayers: 2
Daily Liturgies: 1
```

## 🔧 Configuração

### Variáveis de Ambiente (docker-compose.yml)

```yaml
environment:
  # Database
  DB_CONNECTION: pgsql
  DB_HOST: postgres
  DB_PORT: 5432
  DB_DATABASE: liturgia_db
  DB_USERNAME: postgres
  DB_PASSWORD: "liturgia_db_password_2024_change_this"  # MUDAR
  
  # Flask
  SECRET_KEY: "your-super-secret-key-here"  # MUDAR
  FLASK_ENV: production
```

⚠️ **IMPORTANTE**: Altere `DB_PASSWORD` e `SECRET_KEY` antes do deploy!

### Conexão com PostgreSQL

A aplicação se conecta usando SQLAlchemy:

```python
# Em app.py
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{username}:{password}@{host}:{port}/{database}'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,    # Verifica conexões antes de usar
    'pool_recycle': 300,       # Recicla conexões a cada 5 min
}
```

## 📊 Migrações de Banco

### Flask-Migrate

O projeto usa **Flask-Migrate** (Alembic) para gerenciar alterações no schema:

#### Inicializar Migrações (já feito automaticamente)

```bash
# Dentro do container
flask db init
```

#### Criar Nova Migração

```bash
# Após alterar models/db_models.py
flask db migrate -m "Descrição da mudança"
flask db upgrade
```

#### Reverter Migração

```bash
flask db downgrade
```

## 🔍 Acessar o Banco de Dados

### Via Container

```bash
# Conectar ao container PostgreSQL
POSTGRES_CONTAINER=$(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_postgres")
docker exec -it $POSTGRES_CONTAINER psql -U postgres -d liturgia_db

# Comandos úteis no psql:
liturgia_db=# \dt              # Listar tabelas
liturgia_db=# \d+ celebrations # Descrever tabela
liturgia_db=# SELECT * FROM liturgical_colors;
liturgia_db=# \q               # Sair
```

### Via Python (dentro do container app)

```bash
APP_CONTAINER=$(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_app" | head -1)
docker exec -it $APP_CONTAINER python3

>>> from app import app, db
>>> from models.db_models import *
>>> with app.app_context():
...     colors = LiturgicalColor.query.all()
...     print([c.name for c in colors])
['verde', 'branco', 'vermelho', 'roxo', 'rosa']
```

## 📝 Adicionar Novos Dados

### Via Admin Interface

A aplicação tem interface administrativa em `/admin` para:
- Adicionar novas liturgias
- Gerenciar leituras
- Editar salmos e orações
- Criar missas personalizadas

### Via Script Python

Crie um script `add_data.py`:

```python
from app import app, db
from models.db_models import Celebration, LiturgicalColor
from datetime import date

with app.app_context():
    # Buscar cor
    verde = LiturgicalColor.query.filter_by(name='verde').first()
    
    # Criar celebração
    celebration = Celebration(
        name='Domingo da Semana 3 do Tempo Comum',
        date=date(2026, 1, 25),
        type='feria',
        season='Tempo Comum',
        color=verde
    )
    
    db.session.add(celebration)
    db.session.commit()
    
    print(f"Celebração criada: {celebration.name}")
```

Execute:
```bash
docker exec -it $APP_CONTAINER python3 /var/www/add_data.py
```

## 🔒 Segurança

### Senhas

- ✅ `DB_PASSWORD` hardcoded no docker-compose.yml
- ✅ `SECRET_KEY` hardcoded no docker-compose.yml
- ⚠️ **MUDAR ANTES DO DEPLOY!**

### Conexões

- Pool de conexões com `pool_pre_ping` (detecta conexões mortas)
- Timeout de conexão configurado
- Recycle automático a cada 5 minutos

### SQL Injection

- ✅ Protegido pelo SQLAlchemy ORM
- ✅ Queries parametrizadas automaticamente
- ✅ Sem concatenação de strings SQL

## 📈 Performance

### Índices

- `Celebration.date` (indexed) - para buscar liturgias por data
- `LiturgyHour(date, hour_type)` (unique constraint) - evita duplicatas

### Cache (Redis)

Redis está disponível para cache de queries:

```python
# Exemplo de uso futuro
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': os.environ.get('REDIS_HOST', 'redis'),
    'CACHE_REDIS_PORT': int(os.environ.get('REDIS_PORT', 6379)),
})

@cache.cached(timeout=300)
def get_liturgy(date):
    return DailyLiturgy.query.filter_by(date=date).first()
```

## 🔄 Backup e Restore

### Backup Completo

```bash
# Dump do banco
docker exec $(docker ps -q --filter "name=liturgia_postgres") \
  pg_dump -U postgres liturgia_db > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
# Restaurar backup
cat backup_20260104.sql | \
  docker exec -i $(docker ps -q --filter "name=liturgia_postgres") \
  psql -U postgres liturgia_db
```

### Backup Incremental

O PostgreSQL armazena dados em `/var/lib/postgresql/data/pgdata` (volume `postgres-data`).

## 🧪 Testes

### Testar Conexão

```python
from app import app, db

with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("✓ Database connection OK")
    except Exception as e:
        print(f"✗ Database error: {e}")
```

### Verificar Dados

```python
from app import app, db
from models.db_models import LiturgicalColor, Celebration

with app.app_context():
    colors_count = LiturgicalColor.query.count()
    celebrations_count = Celebration.query.count()
    
    print(f"Colors: {colors_count}")
    print(f"Celebrations: {celebrations_count}")
```

## 📚 Referências

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

## 🆘 Troubleshooting

### Erro: "relation does not exist"

```bash
# Recriar tabelas
docker exec -it $APP_CONTAINER python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Tables created')
"
```

### Erro: "password authentication failed"

Verificar que `DB_PASSWORD` é igual nos dois lugares do docker-compose.yml:
- `app.environment.DB_PASSWORD`
- `postgres.environment.POSTGRES_PASSWORD`

### Container não inicia

```bash
# Ver logs
docker service logs liturgia_app

# Verificar entrypoint
docker service ps liturgia_app --no-trunc
```

### Banco de dados vazio

```bash
# Executar init_db.py manualmente
docker exec -it $APP_CONTAINER python3 /var/www/init_db.py
```
