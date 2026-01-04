# Liturgia - Sistema de Liturgia Diária e Liturgia das Horas

Sistema completo para gerenciamento e personalização de liturgias católicas, incluindo:
- Liturgia Diária (Daily Liturgy)
- Liturgia das Horas (Liturgy of the Hours)
- Personalização completa de missas com todas as suas partes

## Características

- **Liturgia Diária**: Acesso às leituras e orações do dia
- **Liturgia das Horas Completa**: Todas as 7 horas canônicas
  - Ofício das Leituras (Matutino)
  - Laudes (Oração da Manhã)
  - Hora Média: Terça (9h), Sexta (12h), Nona (15h)
  - Vésperas (Oração da Tarde)
  - Completas (Oração da Noite)
- **Personalização Completa de Missas**: 77 partes personalizáveis cobrindo toda a estrutura da Missa:
  - Ritos Iniciais (12 partes)
  - Liturgia da Palavra (14 partes)
  - Liturgia Eucarística (43 partes - incluindo preparação, oração eucarística e comunhão)
  - Ritos Finais (8 partes)

## 🚀 Início Rápido

```bash
# 1. Clone o repositório
git clone https://github.com/josemaeldon/liturgia.git
cd liturgia

# 2. Instale as dependências (opcional, para exportar PDF/DOCX)
pip install -r requirements.txt

# 3. Execute a demonstração
python demo.py

# 4. Ou execute os exemplos
python examples/example_epifania.py          # Missa completa da Epifania
python examples/example_daily_liturgy.py      # Liturgia diária
python examples/example_liturgy_hours.py      # Algumas horas canônicas
python examples/example_all_hours.py          # TODAS as 7 horas canônicas
python examples/example_all_mass_parts.py     # Lista de todas as 77 partes da Missa
python examples/example_custom_mass.py        # Criar missa personalizada
```

## Estrutura do Projeto

```
liturgia/
├── models/          # Modelos de dados para componentes litúrgicos
├── examples/        # Exemplos completos de uso
├── USAGE.md        # Guia detalhado de uso
├── demo.py         # Demonstração do sistema
└── requirements.txt # Dependências opcionais
```

## Uso Básico

### Liturgia Diária

```python
from liturgia import LiturgiaDaily

# Obter liturgia de uma data específica
liturgy = LiturgiaDaily.get_for_date("2026-01-06")  # Epifania do Senhor
print(liturgy.get_full_text())
```

### Liturgia das Horas

```python
from liturgia import LiturgiaHoras

# Obter uma hora específica
laudes = LiturgiaHoras.get_laudes("2026-01-06")
print(laudes.format())

# Obter hora média (Terça, Sexta ou Nona)
terca = LiturgiaHoras.get_terca("2026-01-06")
sexta = LiturgiaHoras.get_sexta("2026-01-06")
nona = LiturgiaHoras.get_nona("2026-01-06")

# Obter todas as 7 horas canônicas de uma vez
all_hours = LiturgiaHoras.get_all_hours("2026-01-06")
# Retorna: {'office_readings', 'laudes', 'terca', 'sexta', 'nona', 'vesperas', 'completas'}

# Ou obter texto formatado de todas as horas
complete_text = LiturgiaHoras.format_all_hours("2026-01-06")
print(complete_text)
```

### Personalização de Missa

```python
from liturgia import CustomMass

# Criar uma missa personalizada
mass = CustomMass()
mass.set_celebration("Solenidade da Epifania do Senhor")
mass.set_entrance_antiphon("Eis que vem o Senhor soberano...")
mass.set_readings(
    first_reading="Is 60,1-6",
    psalm="Sl 71",
    second_reading="Ef 3,2-3a.5-6",
    gospel="Mt 2,1-12"
)
mass.add_custom_prayer("Oração dos Fiéis", custom_text)

# Exportar para diferentes formatos
mass.export_to_pdf("epifania_2026.pdf")
mass.export_to_docx("epifania_2026.docx")
```

## Instalação

**Nenhuma instalação especial necessária!** O sistema funciona apenas com Python 3.8+.

```bash
# Opcional: Para exportar PDF e DOCX
pip install -r requirements.txt
```

## Requisitos

- Python 3.8+
- Bibliotecas listadas em requirements.txt

## 🐳 Deploy em Produção

### 🎯 Stack Completa com PostgreSQL

O sistema está **totalmente integrado com PostgreSQL** e pronto para produção:

✅ **Banco de dados automático** - Tabelas e dados iniciais criados no primeiro deploy  
✅ **Todas as variáveis configuradas** - Sem dependência de arquivos .env  
✅ **Migrations suportadas** - Flask-Migrate para evolução do schema  

### Guias de Deployment

- 🗄️ **[Database Integration: DATABASE_INTEGRATION.md](DATABASE_INTEGRATION.md)** - Como funciona o PostgreSQL
- 🚀 **[Deploy Rápido: QUICK_DEPLOYMENT.md](QUICK_DEPLOYMENT.md)** - Referência rápida e comparação de opções
- 📖 **[PostgreSQL + Apache: POSTGRES_APACHE_DEPLOYMENT.md](POSTGRES_APACHE_DEPLOYMENT.md)** - Stack completa para produção
- 📘 **[Outras Opções: DEPLOYMENT.md](DEPLOYMENT.md)** - Gunicorn, Nginx, Systemd
- 🐋 **[Docker Básico: DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Deploy simples com Docker

### Deploy Rápido (PostgreSQL + Apache + Docker Swarm)

⚠️ **IMPORTANTE**: Edite o `docker-compose.yml` e altere:
- `DB_PASSWORD` (linha 29 e linha 107)
- `SECRET_KEY` (linha 36)

```bash
# 1. Editar senhas no docker-compose.yml
nano docker-compose.yml
# Mudar DB_PASSWORD e SECRET_KEY

# 2. Deploy no Docker Swarm
docker stack deploy -c docker-compose.yml liturgia

# 3. Verificar status
docker stack services liturgia

# 4. Ver logs (aguardar inicialização do banco)
docker service logs -f liturgia_app
```

**O que acontece no primeiro deploy:**
1. PostgreSQL sobe e cria o banco `liturgia_db`
2. App aguarda PostgreSQL ficar pronto
3. Script `init_db.py` cria tabelas e insere dados iniciais
4. Apache inicia e aplicação fica disponível

Veja também:
- [DATABASE_INTEGRATION.md](DATABASE_INTEGRATION.md) - Detalhes do banco de dados
- [DEPLOYMENT.md](DEPLOYMENT.md) - Outras opções de deploy (Gunicorn, Nginx, etc)
- [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) - Deploy básico com Docker

## Exemplos

Veja a pasta `examples/` para exemplos completos de liturgias, incluindo:
- **example_epifania.py** - Missa completa da Solenidade da Epifania (similar ao PDF de referência)
- **example_daily_liturgy.py** - Como usar a liturgia diária
- **example_liturgy_hours.py** - Exemplos de horas canônicas
- **example_all_hours.py** - TODAS as 7 horas canônicas completas
- **example_all_mass_parts.py** - Lista e explicação de todas as 77 partes da Missa
- **example_custom_mass.py** - Como criar missas personalizadas

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests.

## Licença

MIT License