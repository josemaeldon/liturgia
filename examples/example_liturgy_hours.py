"""
Example: Using Liturgy of the Hours functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.liturgy_hours import LiturgiaHoras


def main():
    print("=" * 80)
    print("EXEMPLO: LITURGIA DAS HORAS")
    print("=" * 80)
    
    date = "2026-01-06"
    
    # Office of Readings
    print("\n1. OFÍCIO DAS LEITURAS")
    print("-" * 80)
    office = LiturgiaHoras.get_office_readings(date)
    print(office.format())
    
    # Laudes (Morning Prayer)
    print("\n2. LAUDES (Oração da Manhã)")
    print("-" * 80)
    laudes = LiturgiaHoras.get_laudes(date)
    print(laudes.format())
    
    # Vespers (Evening Prayer)
    print("\n3. VÉSPERAS (Oração da Tarde)")
    print("-" * 80)
    vesperas = LiturgiaHoras.get_vesperas(date)
    print(vesperas.format())
    
    # Compline (Night Prayer)
    print("\n4. COMPLETAS (Oração da Noite)")
    print("-" * 80)
    completas = LiturgiaHoras.get_completas(date)
    print(completas.format())
    
    print("\n\n" + "=" * 80)
    print("Liturgia das Horas completa!")
    print("=" * 80)
    print("\nAs horas canônicas consistem em:")
    print("- Ofício das Leituras (durante a noite ou primeira hora)")
    print("- Laudes (oração da manhã)")
    print("- Hora Média: Terça (9h), Sexta (12h), Nona (15h)")
    print("- Vésperas (oração da tarde)")
    print("- Completas (oração da noite)")


if __name__ == "__main__":
    main()
