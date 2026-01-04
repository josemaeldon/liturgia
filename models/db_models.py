"""
Database models for Liturgia System using SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class LiturgicalColor(db.Model):
    """Liturgical colors table"""
    __tablename__ = 'liturgical_colors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # verde, branco, vermelho, roxo, rosa
    meaning = db.Column(db.Text)
    
    def __repr__(self):
        return f'<LiturgicalColor {self.name}>'


class Celebration(db.Model):
    """Liturgical celebrations table"""
    __tablename__ = 'celebrations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)  # solenidade, festa, memória, feria
    season = db.Column(db.String(50), nullable=False)  # tempo comum, advento, natal, quaresma, páscoa
    color_id = db.Column(db.Integer, db.ForeignKey('liturgical_colors.id'))
    
    # Relationships
    color = db.relationship('LiturgicalColor', backref='celebrations')
    liturgies = db.relationship('DailyLiturgy', back_populates='celebration', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Celebration {self.name} - {self.date}>'


class Reading(db.Model):
    """Biblical readings table"""
    __tablename__ = 'readings'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    book = db.Column(db.String(50))
    chapter = db.Column(db.Integer)
    verses = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reading {self.reference}>'


class Psalm(db.Model):
    """Responsorial psalms table"""
    __tablename__ = 'psalms'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    reference = db.Column(db.String(100), nullable=False)
    response = db.Column(db.Text)
    verses = db.Column(db.Text)  # JSON or text with newlines
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Psalm {self.number}>'


class Prayer(db.Model):
    """Liturgical prayers table"""
    __tablename__ = 'prayers'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    category = db.Column(db.String(50))  # collect, offertory, communion, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prayer {self.title}>'


class DailyLiturgy(db.Model):
    """Daily liturgy table"""
    __tablename__ = 'daily_liturgies'
    
    id = db.Column(db.Integer, primary_key=True)
    celebration_id = db.Column(db.Integer, db.ForeignKey('celebrations.id'), nullable=False)
    first_reading_id = db.Column(db.Integer, db.ForeignKey('readings.id'))
    psalm_id = db.Column(db.Integer, db.ForeignKey('psalms.id'))
    second_reading_id = db.Column(db.Integer, db.ForeignKey('readings.id'))
    gospel_id = db.Column(db.Integer, db.ForeignKey('readings.id'))
    collect_prayer_id = db.Column(db.Integer, db.ForeignKey('prayers.id'))
    offertory_prayer_id = db.Column(db.Integer, db.ForeignKey('prayers.id'))
    communion_prayer_id = db.Column(db.Integer, db.ForeignKey('prayers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    celebration = db.relationship('Celebration', back_populates='liturgies')
    first_reading = db.relationship('Reading', foreign_keys=[first_reading_id])
    psalm = db.relationship('Psalm')
    second_reading = db.relationship('Reading', foreign_keys=[second_reading_id])
    gospel = db.relationship('Reading', foreign_keys=[gospel_id])
    collect_prayer = db.relationship('Prayer', foreign_keys=[collect_prayer_id])
    offertory_prayer = db.relationship('Prayer', foreign_keys=[offertory_prayer_id])
    communion_prayer = db.relationship('Prayer', foreign_keys=[communion_prayer_id])
    
    def __repr__(self):
        return f'<DailyLiturgy {self.celebration.name if self.celebration else "Unknown"}>'


class Antiphon(db.Model):
    """Antiphons table"""
    __tablename__ = 'antiphons'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # entrance, communion, offertory
    text = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(100))
    celebration_id = db.Column(db.Integer, db.ForeignKey('celebrations.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    celebration = db.relationship('Celebration', backref='antiphons')
    
    def __repr__(self):
        return f'<Antiphon {self.type}>'


class LiturgyHour(db.Model):
    """Liturgy of the Hours table"""
    __tablename__ = 'liturgy_hours'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    hour_type = db.Column(db.String(50), nullable=False)  # office_readings, laudes, terca, sexta, nona, vesperas, completas
    content = db.Column(db.JSON)  # Store full hour content as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('date', 'hour_type', name='unique_date_hour'),
    )
    
    def __repr__(self):
        return f'<LiturgyHour {self.hour_type} - {self.date}>'


class CustomMass(db.Model):
    """Custom Mass configurations table"""
    __tablename__ = 'custom_masses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    celebration_name = db.Column(db.String(200))
    celebration_date = db.Column(db.Date)
    celebration_color = db.Column(db.String(50))
    entrance_antiphon = db.Column(db.Text)
    communion_antiphon = db.Column(db.Text)
    custom_prayers = db.Column(db.JSON)  # Store custom prayers as JSON
    readings = db.Column(db.JSON)  # Store readings configuration as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100))  # User identifier (optional)
    
    def __repr__(self):
        return f'<CustomMass {self.name}>'
