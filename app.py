#!/usr/bin/env python3
"""
Flask Web Application for Liturgia System
Modern, responsive interface for daily liturgy and Mass customization
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from datetime import datetime, date, timedelta
import os
import io
from models.daily_liturgy import LiturgiaDaily
from models.liturgy_hours import LiturgiaHoras
from models.custom_mass import CustomMass

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure upload folder for temporary PDF files
# In production, use a secure directory with proper permissions
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/liturgia_pdfs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def index():
    """Home page - Daily liturgy for today"""
    today = date.today()
    return redirect(url_for('daily_liturgy', date_str=today.strftime('%Y-%m-%d')))


@app.route('/liturgia-diaria')
@app.route('/liturgia-diaria/<date_str>')
def daily_liturgy(date_str=None):
    """Display daily liturgy for a specific date"""
    if date_str is None:
        date_str = date.today().strftime('%Y-%m-%d')
    
    try:
        liturgy = LiturgiaDaily.get_for_date(date_str)
        
        # Calculate navigation dates
        current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        prev_date = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
        next_date = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')
        
        return render_template('daily_liturgy.html',
                             liturgy=liturgy,
                             current_date=date_str,
                             prev_date=prev_date,
                             next_date=next_date,
                             today=date.today().strftime('%Y-%m-%d'))
    except Exception as e:
        flash(f'Erro ao carregar liturgia: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/liturgia-horas')
@app.route('/liturgia-horas/<date_str>')
def liturgy_hours(date_str=None):
    """Display Liturgy of the Hours"""
    if date_str is None:
        date_str = date.today().strftime('%Y-%m-%d')
    
    try:
        # Get selected hour from query parameter
        selected_hour = request.args.get('hour', 'laudes')
        
        # Get the selected hour
        hours_map = {
            'office_readings': LiturgiaHoras.get_office_readings,
            'laudes': LiturgiaHoras.get_laudes,
            'terca': LiturgiaHoras.get_terca,
            'sexta': LiturgiaHoras.get_sexta,
            'nona': LiturgiaHoras.get_nona,
            'vesperas': LiturgiaHoras.get_vesperas,
            'completas': LiturgiaHoras.get_completas,
        }
        
        hour_func = hours_map.get(selected_hour, LiturgiaHoras.get_laudes)
        hour_data = hour_func(date_str)
        
        return render_template('liturgy_hours.html',
                             hour_data=hour_data,
                             selected_hour=selected_hour,
                             current_date=date_str,
                             today=date.today().strftime('%Y-%m-%d'))
    except Exception as e:
        flash(f'Erro ao carregar liturgia das horas: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/missa-personalizada', methods=['GET', 'POST'])
def custom_mass():
    """Custom Mass builder and editor"""
    if request.method == 'POST':
        try:
            # Create custom mass from form data
            mass = CustomMass()
            
            # Set celebration details
            celebration_name = request.form.get('celebration_name')
            celebration_date = request.form.get('celebration_date')
            celebration_color = request.form.get('celebration_color', 'verde')
            
            if celebration_name and celebration_date:
                mass.set_celebration(
                    name=celebration_name,
                    date_str=celebration_date,
                    color=celebration_color
                )
            
            # Set readings
            first_reading = request.form.get('first_reading')
            psalm = request.form.get('psalm')
            second_reading = request.form.get('second_reading')
            gospel = request.form.get('gospel')
            
            if first_reading or gospel:
                mass.set_readings(
                    first_reading=first_reading,
                    psalm=psalm,
                    second_reading=second_reading,
                    gospel=gospel
                )
            
            # Set other parts
            entrance_antiphon = request.form.get('entrance_antiphon')
            if entrance_antiphon:
                mass.set_entrance_antiphon(entrance_antiphon)
            
            communion_antiphon = request.form.get('communion_antiphon')
            if communion_antiphon:
                mass.set_communion_antiphon(communion_antiphon)
            
            # Store mass in session or generate preview
            mass_text = mass.get_full_text()
            
            flash('Missa personalizada criada com sucesso!', 'success')
            return render_template('custom_mass_preview.html',
                                 mass=mass,
                                 mass_text=mass_text)
            
        except Exception as e:
            flash(f'Erro ao criar missa: {str(e)}', 'error')
            return redirect(url_for('custom_mass'))
    
    # GET request - show form
    return render_template('custom_mass_form.html',
                         today=date.today().strftime('%Y-%m-%d'))


@app.route('/personalizar-pdf', methods=['GET', 'POST'])
def customize_pdf():
    """PDF customization interface"""
    if request.method == 'POST':
        try:
            # Get customization options
            pdf_options = {
                'font_family': request.form.get('font_family', 'Times-Roman'),
                'font_size': int(request.form.get('font_size', 12)),
                'page_size': request.form.get('page_size', 'A4'),
                'margins': int(request.form.get('margins', 72)),
                'title_size': int(request.form.get('title_size', 18)),
                'include_header': request.form.get('include_header') == 'on',
                'include_footer': request.form.get('include_footer') == 'on',
                'liturgical_color': request.form.get('liturgical_color', 'verde'),
            }
            
            # Get mass data
            mass = CustomMass()
            celebration_name = request.form.get('celebration_name', 'Missa Dominical')
            celebration_date = request.form.get('celebration_date', date.today().strftime('%Y-%m-%d'))
            
            mass.set_celebration(
                name=celebration_name,
                date_str=celebration_date,
                color=pdf_options['liturgical_color']
            )
            
            # Add readings if provided
            first_reading = request.form.get('first_reading')
            gospel = request.form.get('gospel')
            if first_reading or gospel:
                mass.set_readings(
                    first_reading=first_reading,
                    psalm=request.form.get('psalm'),
                    gospel=gospel
                )
            
            # Generate PDF with custom options
            pdf_filename = f"missa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            
            mass.export_to_pdf(pdf_path, **pdf_options)
            
            return send_file(pdf_path,
                           mimetype='application/pdf',
                           as_attachment=True,
                           download_name=f'{celebration_name}.pdf')
            
        except Exception as e:
            flash(f'Erro ao gerar PDF: {str(e)}', 'error')
            return redirect(url_for('customize_pdf'))
    
    # GET request - show customization form
    return render_template('customize_pdf.html',
                         today=date.today().strftime('%Y-%m-%d'))


@app.route('/admin')
def admin():
    """Admin area for content management"""
    return render_template('admin.html')


@app.route('/admin/add-liturgy', methods=['GET', 'POST'])
def add_liturgy():
    """Add new liturgy content"""
    if request.method == 'POST':
        try:
            # Process form data to add new liturgy
            liturgy_date = request.form.get('liturgy_date')
            celebration_name = request.form.get('celebration_name')
            celebration_type = request.form.get('celebration_type')
            liturgical_color = request.form.get('liturgical_color')
            season = request.form.get('season')
            
            # Here you would save to database or file
            # For now, just show success message
            flash(f'Liturgia para {liturgy_date} adicionada com sucesso!', 'success')
            return redirect(url_for('admin'))
            
        except Exception as e:
            flash(f'Erro ao adicionar liturgia: {str(e)}', 'error')
    
    return render_template('add_liturgy.html',
                         today=date.today().strftime('%Y-%m-%d'))


@app.route('/api/liturgy/<date_str>')
def api_liturgy(date_str):
    """API endpoint for liturgy data"""
    try:
        liturgy = LiturgiaDaily.get_for_date(date_str)
        return jsonify({
            'success': True,
            'date': date_str,
            'celebration': liturgy.celebration.name,
            'color': str(liturgy.celebration.color) if liturgy.celebration.color else None,
            'season': liturgy.celebration.season,
            'readings': {
                'first': liturgy.first_reading.reference if liturgy.first_reading else None,
                'psalm': liturgy.psalm.number if liturgy.psalm else None,
                'second': liturgy.second_reading.reference if liturgy.second_reading else None,
                'gospel': liturgy.gospel.reference if liturgy.gospel else None,
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Only use debug mode in development
    # In production, use a WSGI server like gunicorn
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
