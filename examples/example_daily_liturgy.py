"""
Example: Using Daily Liturgy functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.daily_liturgy import LiturgiaDaily


def main():
    print("=" * 80)
    print("EXEMPLO: LITURGIA DIÁRIA")
    print("=" * 80)
    
    # Get liturgy for Epiphany (has specific data)
    print("\n1. Liturgia da Solenidade da Epifania:")
    print("-" * 80)
    epiphany = LiturgiaDaily.get_for_date("2026-01-06")
    print(epiphany.get_full_text())
    
    # Get liturgy for a regular day (will return generic data)
    print("\n\n2. Liturgia de um dia comum:")
    print("-" * 80)
    regular_day = LiturgiaDaily.get_for_date("2026-01-15")
    print(regular_day.get_full_text())
    
    # Add custom liturgy data
    print("\n\n3. Adicionando dados personalizados:")
    print("-" * 80)
    LiturgiaDaily.add_liturgy_data("2026-01-25", {
        "name": "Festa da Conversão de São Paulo",
        "type": "festa",
        "color": "branco",
        "season": "Tempo Comum",
        "first_reading": "At 22,3-16",
        "psalm": "Sl 116(117)",
        "gospel": "Mc 16,15-18"
    })
    
    st_paul = LiturgiaDaily.get_for_date("2026-01-25")
    print(st_paul.get_full_text())
    
    print("\n\n" + "=" * 80)
    print("Exemplo completo!")
    print("=" * 80)


if __name__ == "__main__":
    main()
