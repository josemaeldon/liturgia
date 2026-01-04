"""
Example: Showing all 77 possible parts of the Mass
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.custom_mass import CustomMass


def main():
    print("=" * 80)
    print("TODAS AS 77 PARTES POSSÍVEIS DA SANTA MISSA")
    print("=" * 80)
    
    mass = CustomMass()
    
    # Count and categorize parts
    initial_rites = []
    liturgy_word = []
    liturgy_eucharist = []
    final_rites = []
    
    for key, part in mass.parts.items():
        if part.order <= 12:
            initial_rites.append((part.order, part.title))
        elif part.order <= 26:
            liturgy_word.append((part.order, part.title))
        elif part.order <= 69:
            liturgy_eucharist.append((part.order, part.title))
        else:
            final_rites.append((part.order, part.title))
    
    print("\n" + "=" * 80)
    print("I. RITOS INICIAIS")
    print(f"   ({len(initial_rites)} partes)")
    print("=" * 80)
    for order, title in sorted(initial_rites):
        print(f"{order:2d}. {title}")
    
    print("\n" + "=" * 80)
    print("II. LITURGIA DA PALAVRA")
    print(f"    ({len(liturgy_word)} partes)")
    print("=" * 80)
    for order, title in sorted(liturgy_word):
        print(f"{order:2d}. {title}")
    
    print("\n" + "=" * 80)
    print("III. LITURGIA EUCARÍSTICA")
    print(f"     ({len(liturgy_eucharist)} partes)")
    print("=" * 80)
    
    print("\n  A. Preparação das Oferendas (10 partes)")
    print("  " + "-" * 75)
    for order, title in sorted(liturgy_eucharist)[:10]:
        print(f"  {order:2d}. {title}")
    
    print("\n  B. Oração Eucarística (14 partes)")
    print("  " + "-" * 75)
    for order, title in sorted(liturgy_eucharist)[10:24]:
        print(f"  {order:2d}. {title}")
    
    print("\n  C. Rito da Comunhão (20 partes)")
    print("  " + "-" * 75)
    for order, title in sorted(liturgy_eucharist)[24:]:
        print(f"  {order:2d}. {title}")
    
    print("\n" + "=" * 80)
    print("IV. RITOS FINAIS")
    print(f"    ({len(final_rites)} partes)")
    print("=" * 80)
    for order, title in sorted(final_rites):
        print(f"{order:2d}. {title}")
    
    total = len(initial_rites) + len(liturgy_word) + len(liturgy_eucharist) + len(final_rites)
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {total} PARTES PERSONALIZÁVEIS")
    print("=" * 80)
    
    print("""
DETALHES SOBRE AS PARTES:

RITOS INICIAIS:
- Incluem desde a procissão de entrada até a oração do dia (coleta)
- Partes opcionais: bênção da água, introdução à celebração
- Kyrie pode ser parte do ato penitencial ou separado

LITURGIA DA PALAVRA:
- Leituras, salmo, evangelho com suas procissões e aclamações
- Sequência (apenas em dias especiais: Páscoa, Pentecostes, Corpus Christi, N. Sra. das Dores)
- Homilia e momento de silêncio
- Credo e oração dos fiéis

LITURGIA EUCARÍSTICA:
- Preparação das Oferendas: desde a procissão até a oração sobre as oferendas
  * Inclui preparação do pão e vinho, incensação (opcional), lavabo
- Oração Eucarística: coração da Missa
  * Prefácio, Santo, epicleses, narrativa da instituição, consagração
  * Anamnese, intercessões, doxologia final
- Rito da Comunhão: do Pai Nosso até a oração depois da comunhão
  * Inclui rito da paz, fração do pão, comunhão, purificação dos vasos

RITOS FINAIS:
- Saudação, avisos, bênção (simples ou solene), despedida
- Procissão de saída e canto final

NOTAS IMPORTANTES:
- Nem todas as partes são usadas em todas as missas
- Algumas partes são opcionais (bênção da água, incensação, bênção solene)
- A sequência só é usada em 4 ocasiões especiais durante o ano
- Você pode personalizar qualquer parte usando mass.set_part_content(key, text)
- Ou adicionar partes customizadas com mass.add_custom_prayer(title, text, position)
    """)
    
    print("\n" + "=" * 80)
    print("EXEMPLO DE USO:")
    print("=" * 80)
    print("""
from models.custom_mass import CustomMass

# Criar missa
mass = CustomMass()

# Personalizar qualquer parte pelo nome da chave
mass.set_part_content("entrance_hymn", "Cristo Vive, Cristo Reina...")
mass.set_part_content("consecration_bread", "Isto é o meu Corpo...")
mass.set_part_content("elevation", "Eis o mistério da fé!")

# Ou usar métodos auxiliares
mass.set_entrance_antiphon("Texto da antífona...", "Referência")
mass.set_readings(first_reading="...", gospel="...")

# Exportar
mass.export_to_pdf("missa_completa.pdf")
    """)
    
    print("=" * 80)
    print("Para ver todas as chaves disponíveis:")
    print("  print(list(mass.parts.keys()))")
    print("=" * 80)
    
    # Save list to file
    output_file = os.path.join(os.path.dirname(__file__), "todas_partes_missa.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("LISTA COMPLETA DAS 77 PARTES DA MISSA\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("I. RITOS INICIAIS\n")
        f.write("-" * 80 + "\n")
        for order, title in sorted(initial_rites):
            f.write(f"{order:2d}. {title}\n")
        
        f.write("\nII. LITURGIA DA PALAVRA\n")
        f.write("-" * 80 + "\n")
        for order, title in sorted(liturgy_word):
            f.write(f"{order:2d}. {title}\n")
        
        f.write("\nIII. LITURGIA EUCARÍSTICA\n")
        f.write("-" * 80 + "\n")
        for order, title in sorted(liturgy_eucharist):
            f.write(f"{order:2d}. {title}\n")
        
        f.write("\nIV. RITOS FINAIS\n")
        f.write("-" * 80 + "\n")
        for order, title in sorted(final_rites):
            f.write(f"{order:2d}. {title}\n")
        
        f.write(f"\nTOTAL: {total} partes personalizáveis\n")
    
    print(f"\n✓ Lista completa salva em: {output_file}\n")


if __name__ == "__main__":
    main()
