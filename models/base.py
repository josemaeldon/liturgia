"""
Base models for liturgical components
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date


@dataclass
class Reading:
    """Represents a liturgical reading"""
    reference: str
    text: str = ""
    book: str = ""
    chapter: int = 0
    verses: str = ""
    
    def __str__(self):
        if self.text:
            return f"{self.reference}\n\n{self.text}"
        return self.reference


@dataclass
class Psalm:
    """Represents a responsorial psalm"""
    number: int
    reference: str
    response: str = ""
    verses: List[str] = field(default_factory=list)
    
    def __str__(self):
        result = [f"Salmo {self.number} ({self.reference})"]
        if self.response:
            result.append(f"R. {self.response}")
        for verse in self.verses:
            result.append(verse)
        return "\n".join(result)


@dataclass
class Prayer:
    """Represents a liturgical prayer"""
    title: str
    text: str
    response: str = ""
    
    def __str__(self):
        result = [self.title, "", self.text]
        if self.response:
            result.append(f"R. {self.response}")
        return "\n".join(result)


@dataclass
class Antiphon:
    """Represents an antiphon (entrance, communion, etc.)"""
    type: str  # entrance, communion, offertory
    text: str
    reference: str = ""
    
    def __str__(self):
        result = [f"Antífona de {self.type}", self.text]
        if self.reference:
            result.append(f"({self.reference})")
        return "\n".join(result)


@dataclass
class LiturgicalColor:
    """Represents liturgical colors"""
    name: str  # verde, branco, vermelho, roxo, rosa
    meaning: str = ""
    
    def __str__(self):
        return self.name


@dataclass
class Celebration:
    """Represents a liturgical celebration"""
    name: str
    date: date
    type: str  # solenidade, festa, memória, feria
    color: LiturgicalColor
    season: str  # tempo comum, advento, natal, quaresma, páscoa
    
    def __str__(self):
        return f"{self.name} ({self.type})"
