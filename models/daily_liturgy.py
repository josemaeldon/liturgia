"""
Model for Daily Liturgy
"""

from dataclasses import dataclass
from typing import Optional, Dict
from datetime import date, datetime
from .base import Reading, Psalm, Prayer, Celebration, LiturgicalColor


@dataclass
class DailyLiturgy:
    """Represents the daily liturgy"""
    celebration: Celebration
    first_reading: Optional[Reading] = None
    psalm: Optional[Psalm] = None
    second_reading: Optional[Reading] = None
    gospel: Optional[Reading] = None
    collect_prayer: Optional[Prayer] = None
    offertory_prayer: Optional[Prayer] = None
    communion_prayer: Optional[Prayer] = None
    
    def get_full_text(self) -> str:
        """Get formatted text of the daily liturgy"""
        result = []
        result.append(f"\n{'=' * 80}")
        result.append(f"LITURGIA DIÁRIA - {self.celebration.name.upper()}")
        result.append(f"Data: {self.celebration.date.strftime('%d/%m/%Y')}")
        result.append(f"Cor Litúrgica: {self.celebration.color}")
        result.append(f"Tempo: {self.celebration.season}")
        result.append(f"{'=' * 80}\n")
        
        if self.collect_prayer:
            result.append("\nORAÇÃO DO DIA")
            result.append(str(self.collect_prayer))
        
        if self.first_reading:
            result.append("\nPRIMEIRA LEITURA")
            result.append(str(self.first_reading))
        
        if self.psalm:
            result.append("\nSALMO RESPONSORIAL")
            result.append(str(self.psalm))
        
        if self.second_reading:
            result.append("\nSEGUNDA LEITURA")
            result.append(str(self.second_reading))
        
        if self.gospel:
            result.append("\nEVANGELHO")
            result.append(str(self.gospel))
        
        return "\n".join(result)


class LiturgiaDaily:
    """
    Class to manage and retrieve daily liturgy
    """
    
    # Sample liturgical calendar data
    _calendar: Dict[str, Dict] = {
        "2026-01-06": {
            "name": "Solenidade da Epifania do Senhor",
            "type": "solenidade",
            "color": "branco",
            "season": "Tempo do Natal",
            "first_reading": "Is 60,1-6",
            "psalm": "Sl 71(72)",
            "second_reading": "Ef 3,2-3a.5-6",
            "gospel": "Mt 2,1-12"
        }
    }
    
    @classmethod
    def get_for_date(cls, date_str: str) -> DailyLiturgy:
        """
        Get the daily liturgy for a specific date
        
        Args:
            date_str: Date in format YYYY-MM-DD
            
        Returns:
            DailyLiturgy object with the liturgy for that date
        """
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Check if we have specific data for this date
        if date_str in cls._calendar:
            data = cls._calendar[date_str]
            celebration = Celebration(
                name=data["name"],
                date=liturgy_date,
                type=data["type"],
                color=LiturgicalColor(data["color"]),
                season=data["season"]
            )
            
            first_reading = Reading(reference=data.get("first_reading", ""))
            psalm = Psalm(number=71, reference=data.get("psalm", ""))
            second_reading = Reading(reference=data.get("second_reading", "")) if "second_reading" in data else None
            gospel = Reading(reference=data.get("gospel", ""))
            
            return DailyLiturgy(
                celebration=celebration,
                first_reading=first_reading,
                psalm=psalm,
                second_reading=second_reading,
                gospel=gospel
            )
        else:
            # Return a generic weekday liturgy
            celebration = Celebration(
                name=f"Feria - {liturgy_date.strftime('%d/%m/%Y')}",
                date=liturgy_date,
                type="feria",
                color=LiturgicalColor("verde"),
                season="Tempo Comum"
            )
            
            return DailyLiturgy(celebration=celebration)
    
    @classmethod
    def add_liturgy_data(cls, date_str: str, data: Dict):
        """Add or update liturgy data for a specific date"""
        cls._calendar[date_str] = data
