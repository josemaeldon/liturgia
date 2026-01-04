"""
Model for complete Mass structure with customization capabilities
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import date
from .base import Reading, Psalm, Prayer, Antiphon, Celebration, LiturgicalColor


@dataclass
class MassPart:
    """Represents a part of the Mass"""
    title: str
    content: str
    order: int = 0
    
    def __str__(self):
        return f"\n{self.title}\n{'=' * len(self.title)}\n{self.content}\n"


class CustomMass:
    """
    Represents a fully customizable Catholic Mass with all its parts.
    
    The Mass is structured in four main sections:
    1. Ritos Iniciais (Introductory Rites)
    2. Liturgia da Palavra (Liturgy of the Word)
    3. Liturgia Eucarística (Liturgy of the Eucharist)
    4. Ritos Finais (Concluding Rites)
    """
    
    def __init__(self):
        self.celebration: Optional[Celebration] = None
        self.parts: Dict[str, MassPart] = {}
        self._init_default_structure()
    
    def _init_default_structure(self):
        """Initialize with default Mass structure"""
        # Ritos Iniciais
        self.parts["entrance"] = MassPart("Canto de Entrada", "", 1)
        self.parts["greeting"] = MassPart("Saudação", "Em nome do Pai, do Filho e do Espírito Santo.", 2)
        self.parts["penitential"] = MassPart("Ato Penitencial", "", 3)
        self.parts["kyrie"] = MassPart("Kyrie", "Senhor, tende piedade de nós.", 4)
        self.parts["gloria"] = MassPart("Glória", "", 5)
        self.parts["collect"] = MassPart("Oração do Dia (Coleta)", "", 6)
        
        # Liturgia da Palavra
        self.parts["first_reading"] = MassPart("Primeira Leitura", "", 7)
        self.parts["psalm"] = MassPart("Salmo Responsorial", "", 8)
        self.parts["second_reading"] = MassPart("Segunda Leitura", "", 9)
        self.parts["gospel_acclamation"] = MassPart("Aclamação ao Evangelho", "", 10)
        self.parts["gospel"] = MassPart("Evangelho", "", 11)
        self.parts["homily"] = MassPart("Homilia", "", 12)
        self.parts["creed"] = MassPart("Profissão de Fé (Credo)", "", 13)
        self.parts["prayers_faithful"] = MassPart("Oração dos Fiéis", "", 14)
        
        # Liturgia Eucarística
        self.parts["offertory"] = MassPart("Apresentação das Oferendas", "", 15)
        self.parts["prayer_offerings"] = MassPart("Oração sobre as Oferendas", "", 16)
        self.parts["preface"] = MassPart("Prefácio", "", 17)
        self.parts["sanctus"] = MassPart("Santo", "", 18)
        self.parts["eucharistic_prayer"] = MassPart("Oração Eucarística", "", 19)
        self.parts["our_father"] = MassPart("Pai Nosso", "", 20)
        self.parts["peace"] = MassPart("Rito da Paz", "", 21)
        self.parts["agnus_dei"] = MassPart("Cordeiro de Deus", "", 22)
        self.parts["communion"] = MassPart("Comunhão", "", 23)
        self.parts["communion_antiphon"] = MassPart("Antífona da Comunhão", "", 24)
        self.parts["prayer_communion"] = MassPart("Oração depois da Comunhão", "", 25)
        
        # Ritos Finais
        self.parts["announcements"] = MassPart("Avisos", "", 26)
        self.parts["blessing"] = MassPart("Bênção", "", 27)
        self.parts["dismissal"] = MassPart("Despedida", "", 28)
    
    def set_celebration(self, name: str, date_str: Optional[str] = None, 
                       celebration_type: str = "solenidade",
                       color: str = "branco", season: str = "tempo comum"):
        """Set the celebration details"""
        cel_date = date.today()
        if date_str:
            from datetime import datetime
            cel_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        self.celebration = Celebration(
            name=name,
            date=cel_date,
            type=celebration_type,
            color=LiturgicalColor(color),
            season=season
        )
    
    def set_entrance_antiphon(self, text: str, reference: str = ""):
        """Set the entrance antiphon"""
        antiphon = Antiphon("Entrada", text, reference)
        self.parts["entrance"].content = str(antiphon)
    
    def set_readings(self, first_reading: str = "", psalm: str = "", 
                    second_reading: str = "", gospel: str = ""):
        """Set the readings for the Mass"""
        if first_reading:
            self.parts["first_reading"].content = f"Leitura: {first_reading}"
        if psalm:
            self.parts["psalm"].content = f"Salmo: {psalm}"
        if second_reading:
            self.parts["second_reading"].content = f"Leitura: {second_reading}"
        if gospel:
            self.parts["gospel"].content = f"Evangelho: {gospel}"
    
    def set_part_content(self, part_key: str, content: str):
        """Set content for a specific part of the Mass"""
        if part_key in self.parts:
            self.parts[part_key].content = content
    
    def add_custom_prayer(self, title: str, text: str, position: int = 14):
        """Add a custom prayer at a specific position"""
        key = title.lower().replace(" ", "_")
        self.parts[key] = MassPart(title, text, position)
    
    def get_full_text(self) -> str:
        """Get the complete formatted text of the Mass"""
        result = []
        
        if self.celebration:
            result.append(f"\n{'=' * 80}")
            result.append(f"{self.celebration.name.upper()}")
            result.append(f"Data: {self.celebration.date.strftime('%d/%m/%Y')}")
            result.append(f"Cor Litúrgica: {self.celebration.color}")
            result.append(f"{'=' * 80}\n")
        
        # Sort parts by order
        sorted_parts = sorted(self.parts.values(), key=lambda x: x.order)
        
        for part in sorted_parts:
            if part.content:  # Only include parts with content
                result.append(str(part))
        
        return "\n".join(result)
    
    def export_to_text(self, filename: str):
        """Export the Mass to a text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.get_full_text())
    
    def export_to_pdf(self, filename: str):
        """Export the Mass to PDF format"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Add title
            if self.celebration:
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    textColor='black',
                    spaceAfter=30,
                    alignment=1  # Center
                )
                story.append(Paragraph(self.celebration.name.upper(), title_style))
                story.append(Paragraph(f"Data: {self.celebration.date.strftime('%d/%m/%Y')}", styles['Normal']))
                story.append(Spacer(1, 0.5*inch))
            
            # Add content
            sorted_parts = sorted(self.parts.values(), key=lambda x: x.order)
            for part in sorted_parts:
                if part.content:
                    story.append(Paragraph(f"<b>{part.title}</b>", styles['Heading2']))
                    story.append(Paragraph(part.content.replace('\n', '<br/>'), styles['Normal']))
                    story.append(Spacer(1, 0.2*inch))
            
            doc.build(story)
        except ImportError:
            raise ImportError("reportlab is required for PDF export. Install with: pip install reportlab")
    
    def export_to_docx(self, filename: str):
        """Export the Mass to DOCX format"""
        try:
            from docx import Document
            from docx.shared import Pt, Inches
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            
            doc = Document()
            
            # Add title
            if self.celebration:
                title = doc.add_heading(self.celebration.name.upper(), 0)
                title.alignment = WD_ALIGN_PARAGRAPH.CENTER
                date_para = doc.add_paragraph(f"Data: {self.celebration.date.strftime('%d/%m/%Y')}")
                date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph()
            
            # Add content
            sorted_parts = sorted(self.parts.values(), key=lambda x: x.order)
            for part in sorted_parts:
                if part.content:
                    doc.add_heading(part.title, level=2)
                    doc.add_paragraph(part.content)
            
            doc.save(filename)
        except ImportError:
            raise ImportError("python-docx is required for DOCX export. Install with: pip install python-docx")
