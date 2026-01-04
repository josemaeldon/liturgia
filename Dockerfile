# Dockerfile for Liturgia System
# Production-ready image with Apache and PostgreSQL support for Docker Swarm deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /var/www

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    APACHE_RUN_USER=www-data \
    APACHE_RUN_GROUP=www-data \
    APACHE_LOG_DIR=/var/log/apache2 \
    APACHE_RUN_DIR=/var/run/apache2 \
    APACHE_PID_FILE=/var/run/apache2/apache2.pid \
    APACHE_LOCK_DIR=/var/lock/apache2

# Install system dependencies including Apache, mod_wsgi, and PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    apache2 \
    apache2-dev \
    libapache2-mod-wsgi-py3 \
    gcc \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /var/www/storage \
    /var/www/bootstrap/cache \
    /tmp/liturgia_pdfs \
    ${APACHE_RUN_DIR} \
    ${APACHE_LOCK_DIR} \
    ${APACHE_LOG_DIR}

# Set permissions and make entrypoint executable
RUN chown -R www-data:www-data /var/www /tmp/liturgia_pdfs \
    && chmod -R 755 /var/www \
    && chmod -R 777 /tmp/liturgia_pdfs \
    && chmod +x /var/www/entrypoint.sh

# Create WSGI file
RUN echo 'import sys\n\
import os\n\
\n\
# Add application directory to path\n\
sys.path.insert(0, "/var/www")\n\
\n\
# Import Flask app\n\
from app import app as application\n\
\n\
if __name__ == "__main__":\n\
    application.run()' > /var/www/wsgi.py

# Configure Apache
RUN a2enmod wsgi rewrite headers && \
    echo 'ServerName liturgia' >> /etc/apache2/apache2.conf && \
    echo '<VirtualHost *:80>\n\
    ServerAdmin webmaster@localhost\n\
    DocumentRoot /var/www\n\
    \n\
    WSGIDaemonProcess liturgia user=www-data group=www-data threads=5 python-home=/usr/local\n\
    WSGIScriptAlias / /var/www/wsgi.py\n\
    \n\
    <Directory /var/www>\n\
        WSGIProcessGroup liturgia\n\
        WSGIApplicationGroup %{GLOBAL}\n\
        Require all granted\n\
        Options -Indexes +FollowSymLinks\n\
        AllowOverride All\n\
    </Directory>\n\
    \n\
    <Directory /var/www/static>\n\
        Require all granted\n\
        Options -Indexes\n\
    </Directory>\n\
    \n\
    ErrorLog ${APACHE_LOG_DIR}/error.log\n\
    CustomLog ${APACHE_LOG_DIR}/access.log combined\n\
    \n\
    # Security headers\n\
    Header always set X-Content-Type-Options "nosniff"\n\
    Header always set X-Frame-Options "SAMEORIGIN"\n\
    Header always set X-XSS-Protection "1; mode=block"\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Use entrypoint script to initialize database and start Apache
ENTRYPOINT ["/var/www/entrypoint.sh"]
