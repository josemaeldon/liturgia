#!/usr/bin/env python3
"""
Demo completo do Sistema de Liturgia
Demonstra todas as funcionalidades principais
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.daily_liturgy import LiturgiaDaily
from models.liturgy_hours import LiturgiaHoras
from models.custom_mass import CustomMass


def print_section(title):
    """Helper function to print section headers"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")


def demo_daily_liturgy():
    """Demonstração da Liturgia Diária"""
    print_section("1. LITURGIA DIÁRIA")
    
    # Liturgia de uma solenidade
    liturgy = LiturgiaDaily.get_for_date("2026-01-06")
    print(liturgy.get_full_text())
    print("\n✓ A liturgia diária pode ser consultada por data")
    print("✓ Suporta calendário litúrgico com solenidades, festas e memórias")


def demo_liturgy_hours():
    """Demonstração da Liturgia das Horas"""
    print_section("2. LITURGIA DAS HORAS")
    
    date = "2026-01-06"
    
    # Mostrar apenas Laudes como exemplo
    print("LAUDES (Oração da Manhã)\n")
    laudes = LiturgiaHoras.get_laudes(date)
    print(laudes.format()[:800] + "...\n")
    
    print("✓ Liturgia das Horas completa disponível:")
    print("  • Ofício das Leituras")
    print("  • Laudes (Oração da Manhã)")
    print("  • Hora Média (Terça, Sexta, Nona)")
    print("  • Vésperas (Oração da Tarde)")
    print("  • Completas (Oração da Noite)")


def demo_custom_mass():
    """Demonstração de Missa Personalizada"""
    print_section("3. MISSA PERSONALIZADA")
    
    # Criar missa rápida
    mass = CustomMass()
    mass.set_celebration(
        name="Domingo - Exemplo de Personalização",
        date_str="2026-01-11",
        color="verde"
    )
    
    mass.set_entrance_antiphon(
        "O Senhor é minha luz e salvação, a quem eu temerei?",
        "Sl 26,1"
    )
    
    mass.set_readings(
        first_reading="Is 42,1-4.6-7",
        psalm="Sl 28",
        gospel="Mt 3,13-17"
    )
    
    print("Exemplo de Missa Personalizada (partes principais):\n")
    print(mass.get_full_text()[:1000] + "...\n")
    
    print("✓ 28 partes personalizáveis da missa:")
    print("  • Ritos Iniciais: Entrada, Saudação, Kyrie, Glória, Coleta")
    print("  • Liturgia da Palavra: Leituras, Salmo, Evangelho, Credo, Orações")
    print("  • Liturgia Eucarística: Ofertório, Prefácio, Santo, Oração Eucarística")
    print("  • Ritos Finais: Bênção, Despedida")
    print("\n✓ Exportação para TXT, PDF e DOCX")


def demo_epiphany_example():
    """Demonstração do exemplo completo da Epifania"""
    print_section("4. EXEMPLO COMPLETO: EPIFANIA DO SENHOR")
    
    print("Um exemplo completo da Solenidade da Epifania está disponível em:")
    print("  examples/example_epifania.py")
    print("  examples/epifania_2026.txt (gerado)")
    print("\n✓ Missa completa similar ao PDF de referência")
    print("✓ Todas as partes da missa totalmente preenchidas")
    print("✓ Leituras completas, orações, antífonas, respostas")
    print("✓ Estrutura profissional pronta para uso")


def main():
    """Executa todas as demonstrações"""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SISTEMA DE LITURGIA CATÓLICA" + " " * 30 + "║")
    print("║" + " " * 17 + "Liturgia Diária • Liturgia das Horas • Missa" + " " * 18 + "║")
    print("╚" + "=" * 78 + "╝")
    
    demo_daily_liturgy()
    demo_liturgy_hours()
    demo_custom_mass()
    demo_epiphany_example()
    
    print_section("COMO USAR")
    print("""
1. Liturgia Diária:
   from models.daily_liturgy import LiturgiaDaily
   liturgy = LiturgiaDaily.get_for_date("2026-01-06")
   print(liturgy.get_full_text())

2. Liturgia das Horas:
   from models.liturgy_hours import LiturgiaHoras
   laudes = LiturgiaHoras.get_laudes("2026-01-06")
   print(laudes.format())

3. Missa Personalizada:
   from models.custom_mass import CustomMass
   mass = CustomMass()
   mass.set_celebration("Minha Celebração", "2026-01-06")
   mass.set_readings(first_reading="...", gospel="...")
   mass.export_to_pdf("minha_missa.pdf")

📖 Veja USAGE.md para documentação completa
📁 Veja examples/ para exemplos práticos
    """)
    
    print_section("RECURSOS IMPLEMENTADOS")
    print("""
✓ Sistema completo de Liturgia Diária
✓ Liturgia das Horas (5 horas canônicas)
✓ Missa personalizada com 28 partes configuráveis
✓ Calendário litúrgico
✓ Cores litúrgicas
✓ Exportação para TXT, PDF, DOCX
✓ Exemplos prontos para uso
✓ Documentação completa em português
✓ Estrutura extensível para adicionar mais dados
    """)
    
    print("=" * 80)
    print("Sistema pronto para uso! ✨")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
