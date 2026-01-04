"""
Example: Complete Liturgy of the Hours - All 7 Canonical Hours
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.liturgy_hours import LiturgiaHoras


def main():
    print("=" * 80)
    print("LITURGIA DAS HORAS COMPLETA - TODAS AS 7 HORAS CANÔNICAS")
    print("=" * 80)
    
    date = "2026-01-06"
    
    print("\nA Liturgia das Horas é composta por 7 horas canônicas:\n")
    
    # 1. Office of Readings
    print("\n" + "=" * 80)
    print("1. OFÍCIO DAS LEITURAS")
    print("   Hora: Durante a noite ou primeira hora do dia")
    print("=" * 80)
    office = LiturgiaHoras.get_office_readings(date)
    print(office.format())
    
    # 2. Laudes
    print("\n" + "=" * 80)
    print("2. LAUDES (Oração da Manhã)")
    print("   Hora: Ao amanhecer")
    print("=" * 80)
    laudes = LiturgiaHoras.get_laudes(date)
    print(laudes.format())
    
    # 3. Terça
    print("\n" + "=" * 80)
    print("3. TERÇA (Hora Média - Meio da Manhã)")
    print("   Hora: Por volta das 9h")
    print("=" * 80)
    terca = LiturgiaHoras.get_terca(date)
    print(terca.format())
    
    # 4. Sexta
    print("\n" + "=" * 80)
    print("4. SEXTA (Hora Média - Meio-Dia)")
    print("   Hora: Por volta das 12h")
    print("=" * 80)
    sexta = LiturgiaHoras.get_sexta(date)
    print(sexta.format())
    
    # 5. Nona
    print("\n" + "=" * 80)
    print("5. NONA (Hora Média - Meio da Tarde)")
    print("   Hora: Por volta das 15h")
    print("=" * 80)
    nona = LiturgiaHoras.get_nona(date)
    print(nona.format())
    
    # 6. Vespers
    print("\n" + "=" * 80)
    print("6. VÉSPERAS (Oração da Tarde)")
    print("   Hora: Ao entardecer")
    print("=" * 80)
    vesperas = LiturgiaHoras.get_vesperas(date)
    print(vesperas.format())
    
    # 7. Compline
    print("\n" + "=" * 80)
    print("7. COMPLETAS (Oração da Noite)")
    print("   Hora: Antes de dormir")
    print("=" * 80)
    completas = LiturgiaHoras.get_completas(date)
    print(completas.format())
    
    print("\n\n" + "=" * 80)
    print("RESUMO DAS 7 HORAS CANÔNICAS")
    print("=" * 80)
    print("""
As 7 horas canônicas que compõem a Liturgia das Horas são:

1. OFÍCIO DAS LEITURAS (Matutino)
   - Durante a noite ou primeira hora do dia
   - Leituras mais longas da Escritura e dos Padres da Igreja
   
2. LAUDES (Oração da Manhã)
   - Ao amanhecer
   - Louvor a Deus no início do dia
   
3. HORA MÉDIA - TERÇA
   - Por volta das 9h (meio da manhã)
   - Oração breve durante o trabalho
   
4. HORA MÉDIA - SEXTA
   - Por volta das 12h (meio-dia)
   - Recordação da crucificação de Cristo
   
5. HORA MÉDIA - NONA
   - Por volta das 15h (meio da tarde)
   - Hora da morte de Cristo na cruz
   
6. VÉSPERAS (Oração da Tarde)
   - Ao entardecer
   - Ação de graças pelo dia que passa
   
7. COMPLETAS (Oração da Noite)
   - Antes de dormir
   - Oração de confiança e entrega a Deus
   
NOTA: As horas principais são Laudes e Vésperas.
As Horas Médias (Terça, Sexta, Nona) podem ser rezadas 
uma das três conforme a hora do dia.
    """)
    
    print("=" * 80)
    print("Para obter todas as horas de uma vez:")
    print("  all_hours = LiturgiaHoras.get_all_hours('2026-01-06')")
    print("  text = LiturgiaHoras.format_all_hours('2026-01-06')")
    print("=" * 80)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), "liturgia_horas_completa.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(LiturgiaHoras.format_all_hours(date))
    print(f"\n✓ Liturgia das Horas completa salva em: {output_file}")


if __name__ == "__main__":
    main()
