#!/usr/bin/env python3
"""
Database initialization script
Creates tables and seeds initial data for the Liturgia system
"""

import os
import sys
from datetime import date, datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.db_models import (
    LiturgicalColor, Celebration, Reading, Psalm, Prayer,
    DailyLiturgy, Antiphon, LiturgyHour, CustomMass
)


def init_liturgical_colors():
    """Initialize liturgical colors"""
    print("Initializing liturgical colors...")
    colors = [
        {'name': 'verde', 'meaning': 'Tempo Comum - Esperança e crescimento'},
        {'name': 'branco', 'meaning': 'Natal e Páscoa - Pureza e alegria'},
        {'name': 'vermelho', 'meaning': 'Pentecostes e mártires - Fogo do Espírito Santo'},
        {'name': 'roxo', 'meaning': 'Advento e Quaresma - Penitência e preparação'},
        {'name': 'rosa', 'meaning': 'Gaudete e Laetare - Alegria na preparação'},
    ]
    
    for color_data in colors:
        color = LiturgicalColor.query.filter_by(name=color_data['name']).first()
        if not color:
            color = LiturgicalColor(**color_data)
            db.session.add(color)
            print(f"  Added color: {color_data['name']}")
    
    db.session.commit()
    print("Liturgical colors initialized.")


def init_sample_celebrations():
    """Initialize sample celebrations"""
    print("Initializing sample celebrations...")
    
    verde = LiturgicalColor.query.filter_by(name='verde').first()
    branco = LiturgicalColor.query.filter_by(name='branco').first()
    vermelho = LiturgicalColor.query.filter_by(name='vermelho').first()
    
    celebrations = [
        {
            'name': 'Epifania do Senhor',
            'date': date(2026, 1, 6),
            'type': 'solenidade',
            'season': 'Natal',
            'color': branco
        },
        {
            'name': 'Domingo Ordinário - 2ª Semana',
            'date': date(2026, 1, 18),
            'type': 'feria',
            'season': 'Tempo Comum',
            'color': verde
        },
        {
            'name': 'Pentecostes',
            'date': date(2026, 5, 24),
            'type': 'solenidade',
            'season': 'Páscoa',
            'color': vermelho
        },
    ]
    
    for cel_data in celebrations:
        celebration = Celebration.query.filter_by(
            name=cel_data['name'],
            date=cel_data['date']
        ).first()
        if not celebration:
            celebration = Celebration(**cel_data)
            db.session.add(celebration)
            print(f"  Added celebration: {cel_data['name']}")
    
    db.session.commit()
    print("Sample celebrations initialized.")


def init_sample_readings():
    """Initialize sample readings"""
    print("Initializing sample readings...")
    
    readings = [
        {
            'reference': 'Is 60,1-6',
            'book': 'Isaías',
            'chapter': 60,
            'verses': '1-6',
            'text': 'Levanta-te, acende as lâmpadas, Jerusalém, porque chegou a tua luz...'
        },
        {
            'reference': 'Ef 3,2-3a.5-6',
            'book': 'Efésios',
            'chapter': 3,
            'verses': '2-3a.5-6',
            'text': 'Certamente ouvistes falar da missão da graça de Deus...'
        },
        {
            'reference': 'Mt 2,1-12',
            'book': 'Mateus',
            'chapter': 2,
            'verses': '1-12',
            'text': 'Tendo Jesus nascido em Belém da Judeia...'
        },
    ]
    
    for read_data in readings:
        reading = Reading.query.filter_by(reference=read_data['reference']).first()
        if not reading:
            reading = Reading(**read_data)
            db.session.add(reading)
            print(f"  Added reading: {read_data['reference']}")
    
    db.session.commit()
    print("Sample readings initialized.")


def init_sample_psalms():
    """Initialize sample psalms"""
    print("Initializing sample psalms...")
    
    psalms = [
        {
            'number': 71,
            'reference': 'Sl 71',
            'response': 'Todos os povos, Senhor, hão de adorar-vos',
            'verses': 'V. Ó Deus, dai ao rei vosso julgamento\nV. Nele floresça a justiça nestes dias'
        },
        {
            'number': 23,
            'reference': 'Sl 23',
            'response': 'O Senhor é meu pastor, nada me falta',
            'verses': 'V. O Senhor é meu pastor, nada me falta\nV. Pelos prados verdejantes me conduz'
        },
    ]
    
    for psalm_data in psalms:
        psalm = Psalm.query.filter_by(number=psalm_data['number'], reference=psalm_data['reference']).first()
        if not psalm:
            psalm = Psalm(**psalm_data)
            db.session.add(psalm)
            print(f"  Added psalm: {psalm_data['reference']}")
    
    db.session.commit()
    print("Sample psalms initialized.")


def init_sample_prayers():
    """Initialize sample prayers"""
    print("Initializing sample prayers...")
    
    prayers = [
        {
            'title': 'Oração do Dia - Epifania',
            'text': 'Ó Deus, que neste dia revelastes vosso Filho às nações...',
            'category': 'collect',
            'response': 'Amém'
        },
        {
            'title': 'Oração sobre as Oferendas',
            'text': 'Olhai, ó Deus, as oferendas da vossa Igreja...',
            'category': 'offertory',
            'response': 'Amém'
        },
    ]
    
    for prayer_data in prayers:
        prayer = Prayer.query.filter_by(title=prayer_data['title']).first()
        if not prayer:
            prayer = Prayer(**prayer_data)
            db.session.add(prayer)
            print(f"  Added prayer: {prayer_data['title']}")
    
    db.session.commit()
    print("Sample prayers initialized.")


def init_sample_daily_liturgy():
    """Initialize sample daily liturgy"""
    print("Initializing sample daily liturgy...")
    
    # Get Epiphany celebration
    epifania = Celebration.query.filter_by(name='Epifania do Senhor').first()
    if not epifania:
        print("  Epifania celebration not found, skipping daily liturgy")
        return
    
    # Check if liturgy already exists
    existing = DailyLiturgy.query.filter_by(celebration_id=epifania.id).first()
    if existing:
        print("  Daily liturgy for Epifania already exists")
        return
    
    # Get readings
    first_reading = Reading.query.filter_by(reference='Is 60,1-6').first()
    second_reading = Reading.query.filter_by(reference='Ef 3,2-3a.5-6').first()
    gospel = Reading.query.filter_by(reference='Mt 2,1-12').first()
    psalm = Psalm.query.filter_by(number=71).first()
    collect_prayer = Prayer.query.filter_by(category='collect').first()
    
    liturgy = DailyLiturgy(
        celebration=epifania,
        first_reading=first_reading,
        second_reading=second_reading,
        gospel=gospel,
        psalm=psalm,
        collect_prayer=collect_prayer
    )
    db.session.add(liturgy)
    db.session.commit()
    print("  Added daily liturgy for Epifania")
    print("Sample daily liturgy initialized.")


def initialize_database():
    """Main initialization function"""
    print("=" * 80)
    print("INITIALIZING LITURGIA DATABASE")
    print("=" * 80)
    
    with app.app_context():
        # Create all tables
        print("\nCreating database tables...")
        db.create_all()
        print("Database tables created.")
        
        # Initialize data
        init_liturgical_colors()
        init_sample_celebrations()
        init_sample_readings()
        init_sample_psalms()
        init_sample_prayers()
        init_sample_daily_liturgy()
        
        print("\n" + "=" * 80)
        print("DATABASE INITIALIZATION COMPLETE")
        print("=" * 80)
        
        # Print summary
        print("\nDatabase Summary:")
        print(f"  Liturgical Colors: {LiturgicalColor.query.count()}")
        print(f"  Celebrations: {Celebration.query.count()}")
        print(f"  Readings: {Reading.query.count()}")
        print(f"  Psalms: {Psalm.query.count()}")
        print(f"  Prayers: {Prayer.query.count()}")
        print(f"  Daily Liturgies: {DailyLiturgy.query.count()}")
        print()


if __name__ == '__main__':
    initialize_database()
