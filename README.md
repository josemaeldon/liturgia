# Liturgia - Sistema de Liturgia Diária e Liturgia das Horas

Sistema completo para gerenciamento e personalização de liturgias católicas, incluindo:
- Liturgia Diária (Daily Liturgy)
- Liturgia das Horas (Liturgy of the Hours)
- Personalização completa de missas com todas as suas partes

## Características

- **Liturgia Diária**: Acesso às leituras e orações do dia
- **Liturgia das Horas**: Estrutura completa das horas canônicas (Ofício das Leituras, Laudes, Hora Média, Vésperas, Completas)
- **Personalização de Missas**: Crie e personalize missas completas com todas as partes:
  - Ritos Iniciais (Entrada, Saudação, Ato Penitencial, Kyrie, Glória)
  - Liturgia da Palavra (Leituras, Salmo Responsorial, Evangelho, Homilia, Credo, Oração dos Fiéis)
  - Liturgia Eucarística (Ofertório, Oração Eucarística, Pai Nosso, Comunhão)
  - Ritos Finais (Bênção, Despedida)

## Estrutura do Projeto

```
liturgia/
├── models/          # Modelos de dados para componentes litúrgicos
├── data/           # Dados litúrgicos (leituras, orações, etc.)
├── templates/      # Templates para diferentes tipos de liturgias
├── examples/       # Exemplos de liturgias personalizadas
└── utils/          # Utilitários para formatação e exportação
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

# Obter Laudes do dia
laudes = LiturgiaHoras.get_laudes("2026-01-06")
print(laudes.format())
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

```bash
# Clonar o repositório
git clone https://github.com/josemaeldon/liturgia.git
cd liturgia

# Instalar dependências
pip install -r requirements.txt
```

## Requisitos

- Python 3.8+
- Bibliotecas listadas em requirements.txt

## Exemplos

Veja a pasta `examples/` para exemplos completos de liturgias, incluindo:
- Exemplo de Solenidade da Epifania (similar ao PDF de referência)
- Liturgias dominicais
- Liturgia das Horas completa

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests.

## Licença

MIT License