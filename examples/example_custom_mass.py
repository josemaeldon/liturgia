"""
Example: Creating a Custom Mass from scratch
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.custom_mass import CustomMass


def main():
    print("=" * 80)
    print("EXEMPLO: CRIANDO UMA MISSA PERSONALIZADA")
    print("=" * 80)
    
    # Create a new custom Mass
    mass = CustomMass()
    
    # Set basic celebration info
    mass.set_celebration(
        name="II Domingo do Tempo Comum",
        date_str="2026-01-18",
        celebration_type="domingo",
        color="verde",
        season="Tempo Comum"
    )
    
    # Customize entrance
    mass.set_entrance_antiphon(
        text="Toda a terra vos adore, ó Deus, e cante salmos ao vosso nome, ó Altíssimo!",
        reference="Sl 65,4"
    )
    
    # Set readings
    mass.set_readings(
        first_reading="Is 49,3.5-6",
        psalm="Sl 39(40)",
        second_reading="1Cor 1,1-3",
        gospel="Jo 1,29-34"
    )
    
    # Add custom collect prayer
    mass.set_part_content("collect",
        "Oremos.\n\n"
        "Deus eterno e todo-poderoso, que presidis a todo o universo, "
        "atendei, na vossa bondade, às súplicas do vosso povo, "
        "e fazei que estes nossos dias se passem na vossa paz.\n"
        "Por nosso Senhor Jesus Cristo, vosso Filho, na unidade do Espírito Santo.\n\n"
        "R. Amém."
    )
    
    # Add custom prayers of the faithful
    mass.set_part_content("prayers_faithful",
        "Roguemos a Deus Pai todo-poderoso:\n"
        "R. Senhor, escutai a nossa oração!\n\n"
        "1. Pela santa Igreja de Deus, para que seja luz e sal da terra. "
        "Roguemos ao Senhor. R.\n\n"
        "2. Pelos governantes, para que promovam a justiça e o bem comum. "
        "Roguemos ao Senhor. R.\n\n"
        "3. Pelos enfermos e sofredores, para que encontrem consolo e esperança. "
        "Roguemos ao Senhor. R.\n\n"
        "4. Por nossa comunidade, para que cresçamos na fé e no amor fraterno. "
        "Roguemos ao Senhor. R.\n\n"
        "Ó Deus, que acolheis com bondade as preces do vosso povo, "
        "concedei-nos o que pedimos com fé. "
        "Por Cristo, nosso Senhor. R. Amém."
    )
    
    # Add communion antiphon
    mass.set_part_content("communion_antiphon",
        "Antífona da Comunhão\n\n"
        "Senhor, preparastes uma mesa para mim, "
        "e transborda minha taça.\n"
        "(Sl 22,5)"
    )
    
    # Display the complete Mass
    print("\n")
    print(mass.get_full_text())
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), "missa_personalizada.txt")
    mass.export_to_text(output_file)
    print(f"\n\nMissa salva em: {output_file}")
    
    print("\n" + "=" * 80)
    print("Missa personalizada criada com sucesso!")
    print("=" * 80)
    print("\nVocê pode personalizar:")
    print("- Todas as partes da missa")
    print("- Leituras e orações")
    print("- Antífonas e respostas")
    print("- Exportar para TXT, PDF ou DOCX")


if __name__ == "__main__":
    main()
