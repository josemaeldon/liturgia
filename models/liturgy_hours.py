"""
Model for Liturgy of the Hours (Liturgia das Horas)
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, datetime
from .base import Psalm, Prayer, Antiphon, Celebration


@dataclass
class Hour:
    """Represents one of the canonical hours"""
    name: str
    time: str
    hymn: Optional[str] = None
    psalms: List[Psalm] = field(default_factory=list)
    antiphons: List[str] = field(default_factory=list)
    reading: Optional[str] = None
    canticle: Optional[str] = None
    prayers: List[Prayer] = field(default_factory=list)
    
    def format(self) -> str:
        """Format the hour for display"""
        result = []
        result.append(f"\n{'=' * 80}")
        result.append(f"{self.name.upper()}")
        result.append(f"Hora: {self.time}")
        result.append(f"{'=' * 80}\n")
        
        if self.hymn:
            result.append("HINO")
            result.append(self.hymn)
            result.append("")
        
        if self.psalms:
            result.append("SALMODIA")
            for i, (psalm, antiphon) in enumerate(zip(self.psalms, self.antiphons), 1):
                if antiphon:
                    result.append(f"\nAnt. {i}: {antiphon}")
                result.append(str(psalm))
            result.append("")
        
        if self.reading:
            result.append("LEITURA BREVE")
            result.append(self.reading)
            result.append("")
        
        if self.canticle:
            result.append("CÂNTICO")
            result.append(self.canticle)
            result.append("")
        
        if self.prayers:
            for prayer in self.prayers:
                result.append(str(prayer))
                result.append("")
        
        return "\n".join(result)


class LiturgiaHoras:
    """
    Class to manage the Liturgy of the Hours
    
    The complete Liturgy of the Hours consists of:
    - Ofício das Leituras (Office of Readings)
    - Laudes (Morning Prayer)
    - Hora Média (Midday Prayer):
      - Terça (Mid-Morning Prayer - 9h)
      - Sexta (Midday Prayer - 12h)
      - Nona (Mid-Afternoon Prayer - 15h)
    - Vésperas (Evening Prayer)
    - Completas (Night Prayer)
    """
    
    @classmethod
    def get_office_readings(cls, date_str: str) -> Hour:
        """Get Office of Readings for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        office = Hour(
            name="Ofício das Leituras",
            time="Durante a noite ou primeira hora do dia",
            hymn="Da luz primeira, Criador,\nque separaste a treva do esplendor...",
            psalms=[
                Psalm(number=1, reference="Sl 1",
                      response="Feliz o homem que ama a lei do Senhor.",
                      verses=["Feliz o homem que não se guia..."]),
                Psalm(number=2, reference="Sl 2",
                      response="Felizes os que no Senhor se refugiam.",
                      verses=["Por que se agitam as nações..."])
            ],
            antiphons=[
                "A minha boca anunciará vosso louvor",
                "Adoremos ao Senhor, que nos criou"
            ],
            reading="Primeira Leitura: Leitura longa da Sagrada Escritura\nSegunda Leitura: Leitura dos Santos Padres ou escritores eclesiásticos",
            prayers=[
                Prayer(
                    title="Oração Final",
                    text="Deus eterno e todo-poderoso, que nos congregais para rezarmos no início deste dia..."
                )
            ]
        )
        
        return office
    
    @classmethod
    def get_laudes(cls, date_str: str) -> Hour:
        """Get Laudes (Morning Prayer) for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Create a sample Laudes
        laudes = Hour(
            name="Laudes (Oração da Manhã)",
            time="Ao amanhecer",
            hymn="Ó Cristo, sol da verdade,\nque iluminas o universo,\nda tua imensa bondade\na luz vem, sempre diversa.",
            psalms=[
                Psalm(number=63, reference="Sl 63,2-9", 
                      response="Minha alma tem sede de Vós, ó Senhor.",
                      verses=["Ó Deus, vós sois o meu Deus, eu vos procuro..."]),
                Psalm(number=149, reference="Sl 149",
                      response="O Senhor ama o seu povo.",
                      verses=["Cantai ao Senhor Deus um canto novo..."])
            ],
            antiphons=[
                "Bendizei ao Senhor todas as suas obras",
                "Que tudo quanto existe cante um hino ao Senhor"
            ],
            reading="Leitura breve: Rm 13,11-12a",
            canticle="Benedictus - Cântico de Zacarias (Lc 1,68-79)",
            prayers=[
                Prayer(
                    title="Preces",
                    text="Oremos ao Senhor que nos criou para louvarmos seu nome...",
                    response="Senhor, tende piedade de nós"
                ),
                Prayer(
                    title="Oração Final",
                    text="Pai santo, dai-nos neste novo dia a graça de vos servir com alegria..."
                )
            ]
        )
        
        return laudes
    
    @classmethod
    def get_terca(cls, date_str: str) -> Hour:
        """Get Terça (Mid-Morning Prayer - 9h) for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        terca = Hour(
            name="Terça (Hora Média - Meio da Manhã)",
            time="Por volta das 9 horas",
            hymn="Agora que o dia avança,\nimploramos, Senhor,\nque nos guardes de toda ofensa\ne nos dês teu amor.",
            psalms=[
                Psalm(number=119, reference="Sl 119(120),1-7",
                      response="A ti, Senhor, ergo os meus olhos.",
                      verses=["Levanto os olhos para os montes..."]),
                Psalm(number=120, reference="Sl 120(121)",
                      response="O Senhor é teu guarda e proteção.",
                      verses=["Levanto os olhos para os montes..."])
            ],
            antiphons=[
                "A ti, Senhor, clamei em minha aflição",
                "O Senhor é teu guarda e proteção"
            ],
            reading="Leitura breve: Dt 6,4-7\n\nOuve, ó Israel! O Senhor, nosso Deus, é o único Senhor. "
                    "Amarás ao Senhor, teu Deus, de todo o teu coração, de toda a tua alma e com todas as tuas forças.",
            prayers=[
                Prayer(
                    title="Oração da Hora",
                    text="Ó Deus, que pela luz do Espírito Santo instruís os corações dos fiéis, "
                         "concedei-nos que, no mesmo Espírito, conheçamos o que é reto "
                         "e gozemos sempre de suas consolações. Por Cristo, nosso Senhor.",
                    response="Amém"
                )
            ]
        )
        
        return terca
    
    @classmethod
    def get_sexta(cls, date_str: str) -> Hour:
        """Get Sexta (Midday Prayer - 12h) for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        sexta = Hour(
            name="Sexta (Hora Média - Meio-Dia)",
            time="Por volta das 12 horas",
            hymn="Ó Cristo, Rei do universo,\nvinde, em teu poder imerso,\ndefender vossos servos,\ndar-lhes a paz e o verso.",
            psalms=[
                Psalm(number=122, reference="Sl 122(123)",
                      response="Os nossos olhos estão no Senhor.",
                      verses=["A ti levanto os meus olhos, a ti que habitas nos céus..."]),
                Psalm(number=123, reference="Sl 123(124)",
                      response="O nosso auxílio está no nome do Senhor.",
                      verses=["Se o Senhor não estivesse do nosso lado..."])
            ],
            antiphons=[
                "Os nossos olhos no Senhor, até que se compadeça de nós",
                "O nosso auxílio está no nome do Senhor"
            ],
            reading="Leitura breve: Tg 2,12-13\n\nFalai e agi como quem vai ser julgado pela lei da liberdade. "
                    "Porque o juízo será sem misericórdia para quem não usou de misericórdia; "
                    "mas a misericórdia triunfa sobre o juízo.",
            prayers=[
                Prayer(
                    title="Oração da Hora",
                    text="Ó Deus, que para remir o mundo quisestes nascer e ser circuncidado, "
                         "ser rejeitado pelos judeus e traído por Judas com um beijo, "
                         "ser amarrado com cordas, levado como cordeiro ao sacrifício, "
                         "apresentado a Anás, Caifás, Pilatos e Herodes, acusado por falsas testemunhas, "
                         "flagelado e ultrajado; protegei-nos, em vossa bondade, de todos os males do corpo e da alma. "
                         "Por Cristo, nosso Senhor.",
                    response="Amém"
                )
            ]
        )
        
        return sexta
    
    @classmethod
    def get_nona(cls, date_str: str) -> Hour:
        """Get Nona (Mid-Afternoon Prayer - 15h) for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        nona = Hour(
            name="Nona (Hora Média - Meio da Tarde)",
            time="Por volta das 15 horas",
            hymn="Quando a tarde vai caindo,\nque teu brilho, ó Redentor,\nem nossos corações infindo,\nacenda a chama do amor.",
            psalms=[
                Psalm(number=124, reference="Sl 124(125)",
                      response="Quem confia no Senhor é como o monte Sião.",
                      verses=["Os que confiam no Senhor são como o monte de Sião..."]),
                Psalm(number=125, reference="Sl 125(126)",
                      response="O Senhor fez por nós maravilhas.",
                      verses=["Quando o Senhor reconduziu os cativos de Sião..."])
            ],
            antiphons=[
                "Quem confia no Senhor jamais será abalado",
                "Fazei, Senhor, maravilhas, enchei-nos de alegria"
            ],
            reading="Leitura breve: 1Pd 5,8-9\n\nSede sóbrios e vigiai. Vosso adversário, o demônio, "
                    "anda ao redor de vós como leão que ruge, buscando a quem devorar. "
                    "Resisti-lhe, firmes na fé.",
            prayers=[
                Prayer(
                    title="Oração da Hora",
                    text="Ó Deus, que pela morte preciosa de vosso Filho na Cruz, "
                         "à hora de Nona, nos livrastes da morte eterna, "
                         "concedei-nos chegarmos, purificados, à glória da ressurreição. "
                         "Por Cristo, nosso Senhor.",
                    response="Amém"
                )
            ]
        )
        
        return nona
    
    @classmethod
    def get_vesperas(cls, date_str: str) -> Hour:
        """Get Vésperas (Evening Prayer) for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        vesperas = Hour(
            name="Vésperas (Oração da Tarde)",
            time="Ao entardecer",
            hymn="Ó Cristo, luz do mundo,\nque a noite se aproxima,\nacendei em nós o fogo\nda caridade divina.",
            psalms=[
                Psalm(number=141, reference="Sl 141(142)",
                      response="Suba minha oração, como incenso, à vossa presença.",
                      verses=["Senhor, a vós clamo: vinde depressa..."]),
                Psalm(number=110, reference="Sl 110(111)",
                      response="Grandes são as obras do Senhor.",
                      verses=["De todo coração agradeço ao Senhor..."])
            ],
            antiphons=[
                "Como incenso suba a vós minha oração",
                "Bendito seja Deus, agora e sempre"
            ],
            reading="Leitura breve: 1 Pd 1,3-5",
            canticle="Magnificat - Cântico de Maria (Lc 1,46-55)",
            prayers=[
                Prayer(
                    title="Preces",
                    text="Oremos nesta hora em que Cristo, pendurado na cruz, nos abriu as portas da salvação...",
                    response="Senhor, escutai nossa oração"
                ),
                Prayer(
                    title="Pai Nosso",
                    text="Rezemos ao Pai como Jesus nos ensinou..."
                ),
                Prayer(
                    title="Oração Final",
                    text="Concedei-nos, ó Deus, que esta noite transcorra em santa paz..."
                )
            ]
        )
        
        return vesperas
    
    @classmethod
    def get_completas(cls, date_str: str) -> Hour:
        """Get Completas (Night Prayer) for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        completas = Hour(
            name="Completas (Oração da Noite)",
            time="Antes de dormir",
            hymn="Antes que a noite desça,\na ti, Senhor, recorro;\nguarda-me nesta treva,\nde todo mal socorro.",
            psalms=[
                Psalm(number=91, reference="Sl 91(92)",
                      response="Habita à sombra do Onipotente.",
                      verses=["Aquele que no abrigo do Altíssimo reside..."])
            ],
            antiphons=[
                "Em tuas mãos, Senhor, entrego meu espírito"
            ],
            reading="Leitura breve: Jr 14,9b",
            canticle="Nunc Dimittis - Cântico de Simeão (Lc 2,29-32)",
            prayers=[
                Prayer(
                    title="Oração Final",
                    text="Concedei-nos, Deus todo-poderoso, uma noite tranquila e um fim perfeito."
                )
            ]
        )
        
        return completas
    
    @classmethod
    def get_office_readings(cls, date_str: str) -> Hour:
        """Get Office of Readings for a specific date"""
        liturgy_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        office = Hour(
            name="Ofício das Leituras",
            time="Durante a noite ou primeira hora do dia",
            hymn="Da luz primeira, Criador,\nque separaste a treva do esplendor...",
            psalms=[
                Psalm(number=1, reference="Sl 1",
                      response="Feliz o homem que ama a lei do Senhor.",
                      verses=["Feliz o homem que não se guia..."]),
                Psalm(number=2, reference="Sl 2",
                      response="Felizes os que no Senhor se refugiam.",
                      verses=["Por que se agitam as nações..."])
            ],
            antiphons=[
                "A minha boca anunciará vosso louvor",
                "Adoremos ao Senhor, que nos criou"
            ],
            reading="Primeira Leitura: Leitura longa da Sagrada Escritura\nSegunda Leitura: Leitura dos Santos Padres ou escritores eclesiásticos",
            prayers=[
                Prayer(
                    title="Oração Final",
                    text="Deus eterno e todo-poderoso, que nos congregais para rezarmos no início deste dia..."
                )
            ]
        )
        
        return office


    @classmethod
    def get_all_hours(cls, date_str: str) -> dict:
        """
        Get all canonical hours for a specific date
        
        Returns:
            Dictionary with all hours: {
                'office_readings': Hour,
                'laudes': Hour,
                'terca': Hour,
                'sexta': Hour,
                'nona': Hour,
                'vesperas': Hour,
                'completas': Hour
            }
        """
        return {
            'office_readings': cls.get_office_readings(date_str),
            'laudes': cls.get_laudes(date_str),
            'terca': cls.get_terca(date_str),
            'sexta': cls.get_sexta(date_str),
            'nona': cls.get_nona(date_str),
            'vesperas': cls.get_vesperas(date_str),
            'completas': cls.get_completas(date_str)
        }
    
    @classmethod
    def format_all_hours(cls, date_str: str) -> str:
        """Get formatted text of all canonical hours for a date"""
        all_hours = cls.get_all_hours(date_str)
        result = []
        result.append("\n" + "=" * 80)
        result.append("LITURGIA DAS HORAS COMPLETA")
        result.append(f"Data: {date_str}")
        result.append("=" * 80)
        
        for hour_name, hour in all_hours.items():
            result.append(hour.format())
            result.append("\n" + "-" * 80 + "\n")
        
        return "\n".join(result)

