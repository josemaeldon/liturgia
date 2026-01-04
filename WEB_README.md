# Liturgia Católica - Web Application

Modern and responsive web interface for the Catholic Liturgy system.

## Features

### 1. Daily Liturgy (Liturgia Diária)
- View today's liturgy with readings and prayers
- Navigate between dates
- Display liturgical colors following the Roman Missal
- Responsive design for mobile and desktop

### 2. Liturgy of the Hours (Liturgia das Horas)
- Access all 7 canonical hours:
  - Office of Readings (Matins)
  - Lauds (Morning Prayer)
  - Terce, Sext, None (Mid-day prayers)
  - Vespers (Evening Prayer)
  - Compline (Night Prayer)

### 3. Custom Mass Builder (Missa Personalizada)
- Create personalized Mass celebrations
- Add all readings and prayers
- Customize entrance and communion antiphons
- Export to various formats

### 4. PDF Customization (Personalizar PDF)
- Professional Mass leaflet generator
- Customizable fonts, sizes, and layouts
- Multiple page size options (A4, Letter, A5)
- Liturgical color indicators
- Ready for printing

### 5. Admin Area (Área Administrativa)
- Content management system
- Add new liturgies to the calendar
- Manage readings, psalms, and prayers
- Configure liturgical calendar

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **PDF Generation**: ReportLab
- **Icons**: Bootstrap Icons
- **Fonts**: Google Fonts (Lora, Inter)

## Design Features

- **Responsive**: Works on all screen sizes (mobile, tablet, desktop)
- **Modern**: Clean and contemporary design
- **Accessible**: Easy navigation and clear typography
- **Professional**: Liturgical color coding and proper formatting

## Project Structure

```
liturgia/
├── app.py                      # Flask application
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── daily_liturgy.html     # Daily liturgy page
│   ├── liturgy_hours.html     # Liturgy of Hours page
│   ├── custom_mass_form.html  # Custom Mass form
│   ├── custom_mass_preview.html # Mass preview
│   ├── customize_pdf.html     # PDF customization
│   ├── admin.html             # Admin dashboard
│   ├── add_liturgy.html       # Add liturgy form
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Custom CSS
│   └── js/
│       └── main.js            # Custom JavaScript
└── models/                     # Data models
    ├── daily_liturgy.py
    ├── liturgy_hours.py
    └── custom_mass.py
```

## API Endpoints

- `GET /` - Home page (redirects to daily liturgy)
- `GET /liturgia-diaria` - Today's liturgy
- `GET /liturgia-diaria/<date>` - Liturgy for specific date
- `GET /liturgia-horas` - Liturgy of the Hours
- `GET /missa-personalizada` - Custom Mass form
- `POST /missa-personalizada` - Create custom Mass
- `GET /personalizar-pdf` - PDF customization page
- `POST /personalizar-pdf` - Generate PDF
- `GET /admin` - Admin dashboard
- `GET /api/liturgy/<date>` - API endpoint for liturgy data

## Liturgical Calendar

The system follows the Roman Missal cycles:
- Liturgical seasons (Advent, Christmas, Lent, Easter, Ordinary Time)
- Liturgical colors (White, Red, Green, Purple, Gold, Black)
- Celebration types (Solemnities, Feasts, Memorials, Ferias)

## PDF Export Options

- Font family (Times Roman, Helvetica, Courier)
- Font size (8-16pt)
- Title size (14-24pt)
- Page size (A4, Letter, A5)
- Margins (customizable)
- Header/Footer options
- Liturgical color accents

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

The application will run with debug mode enabled and auto-reload on code changes.

## Production Deployment

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

MIT License

## Credits

Developed following the Roman Missal and Liturgy of the Hours guidelines.
