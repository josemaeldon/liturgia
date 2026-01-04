# Guia de Uso - Sistema de Liturgia

Este guia mostra como usar o sistema de liturgia para criar e gerenciar liturgias católicas.

## Instalação

```bash
# Clone o repositório
git clone https://github.com/josemaeldon/liturgia.git
cd liturgia

# Instale as dependências
pip install -r requirements.txt
```

## 1. Liturgia Diária

### Uso Básico

```python
from models.daily_liturgy import LiturgiaDaily

# Obter liturgia de uma data específica
liturgy = LiturgiaDaily.get_for_date("2026-01-06")
print(liturgy.get_full_text())
```

### Adicionar Dados Personalizados

```python
# Adicionar nova liturgia ao calendário
LiturgiaDaily.add_liturgy_data("2026-02-02", {
    "name": "Apresentação do Senhor",
    "type": "festa",
    "color": "branco",
    "season": "Tempo Comum",
    "first_reading": "Ml 3,1-4",
    "psalm": "Sl 23(24)",
    "second_reading": "Hb 2,14-18",
    "gospel": "Lc 2,22-40"
})
```

## 2. Liturgia das Horas

### Ofício das Leituras

```python
from models.liturgy_hours import LiturgiaHoras

office = LiturgiaHoras.get_office_readings("2026-01-06")
print(office.format())
```

### Laudes (Oração da Manhã)

```python
laudes = LiturgiaHoras.get_laudes("2026-01-06")
print(laudes.format())
```

### Vésperas (Oração da Tarde)

```python
vesperas = LiturgiaHoras.get_vesperas("2026-01-06")
print(vesperas.format())
```

### Completas (Oração da Noite)

```python
completas = LiturgiaHoras.get_completas("2026-01-06")
print(completas.format())
```

## 3. Missa Personalizada

### Criar uma Missa Completa

```python
from models.custom_mass import CustomMass

# Criar nova missa
mass = CustomMass()

# Definir celebração
mass.set_celebration(
    name="Solenidade da Epifania do Senhor",
    date_str="2026-01-06",
    celebration_type="solenidade",
    color="branco",
    season="Tempo do Natal"
)

# Definir antífona de entrada
mass.set_entrance_antiphon(
    text="Eis que vem o Senhor soberano...",
    reference="Cf. Ml 3,1"
)

# Definir leituras
mass.set_readings(
    first_reading="Is 60,1-6",
    psalm="Sl 71",
    second_reading="Ef 3,2-3a.5-6",
    gospel="Mt 2,1-12"
)

# Personalizar qualquer parte
mass.set_part_content("collect", "Texto da oração do dia...")
mass.set_part_content("prayers_faithful", "Orações dos fiéis...")

# Obter texto completo
print(mass.get_full_text())
```

### Exportar para Diferentes Formatos

```python
# Exportar para texto
mass.export_to_text("minha_missa.txt")

# Exportar para PDF (requer reportlab)
mass.export_to_pdf("minha_missa.pdf")

# Exportar para DOCX (requer python-docx)
mass.export_to_docx("minha_missa.docx")
```

## 4. Estrutura da Missa

A missa é organizada em quatro seções principais:

### Ritos Iniciais
1. Canto de Entrada (entrance)
2. Saudação (greeting)
3. Ato Penitencial (penitential)
4. Kyrie (kyrie)
5. Glória (gloria)
6. Oração do Dia/Coleta (collect)

### Liturgia da Palavra
7. Primeira Leitura (first_reading)
8. Salmo Responsorial (psalm)
9. Segunda Leitura (second_reading) - opcional
10. Aclamação ao Evangelho (gospel_acclamation)
11. Evangelho (gospel)
12. Homilia (homily)
13. Profissão de Fé/Credo (creed)
14. Oração dos Fiéis (prayers_faithful)

### Liturgia Eucarística
15. Apresentação das Oferendas (offertory)
16. Oração sobre as Oferendas (prayer_offerings)
17. Prefácio (preface)
18. Santo (sanctus)
19. Oração Eucarística (eucharistic_prayer)
20. Pai Nosso (our_father)
21. Rito da Paz (peace)
22. Cordeiro de Deus (agnus_dei)
23. Comunhão (communion)
24. Antífona da Comunhão (communion_antiphon)
25. Oração depois da Comunhão (prayer_communion)

### Ritos Finais
26. Avisos (announcements)
27. Bênção (blessing)
28. Despedida (dismissal)

## 5. Personalização Avançada

### Adicionar Orações Personalizadas

```python
# Adicionar uma oração em posição específica
mass.add_custom_prayer(
    title="Oração Especial",
    text="Texto da oração...",
    position=15  # Posição na ordem da missa
)
```

### Modificar Partes Existentes

```python
# Acessar partes diretamente
mass.parts["collect"].content = "Nova oração do dia..."
mass.parts["gospel"].content = "Novo texto do evangelho..."
```

## 6. Exemplos Completos

Veja a pasta `examples/` para exemplos completos:

- `example_epifania.py` - Missa completa da Epifania (similar ao PDF de referência)
- `example_daily_liturgy.py` - Uso da liturgia diária
- `example_liturgy_hours.py` - Uso da liturgia das horas
- `example_custom_mass.py` - Criação de missa personalizada

## 7. Executar os Exemplos

```bash
# Da raiz do projeto
python examples/example_epifania.py
python examples/example_daily_liturgy.py
python examples/example_liturgy_hours.py
python examples/example_custom_mass.py
```

## 8. Cores Litúrgicas

- **Branco**: Natal, Páscoa, festas do Senhor, Maria e santos não mártires
- **Vermelho**: Domingo de Ramos, Sexta-feira Santa, Pentecostes, festas dos mártires
- **Verde**: Tempo Comum
- **Roxo**: Advento, Quaresma
- **Rosa**: 3º Domingo do Advento, 4º Domingo da Quaresma

## 9. Tipos de Celebrações

- **Solenidade**: Celebrações mais importantes (Natal, Páscoa, etc.)
- **Festa**: Celebrações de santos importantes
- **Memória Obrigatória**: Memórias que devem ser celebradas
- **Memória Facultativa**: Memórias opcionais
- **Feria**: Dias de semana comuns

## Dúvidas?

Para mais informações ou contribuições, acesse:
https://github.com/josemaeldon/liturgia
