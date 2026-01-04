# Deployment Guide - Liturgia Católica Web Application

This guide covers deployment options for the Liturgia Católica web application.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Production Deployment](#production-deployment)
4. [Environment Variables](#environment-variables)
5. [Security Considerations](#security-considerations)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/josemaeldon/liturgia.git
cd liturgia
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (Optional)

```bash
# Development settings
export FLASK_DEBUG=true
export SECRET_KEY=dev-secret-key-change-me
export UPLOAD_FOLDER=/tmp/liturgia_pdfs
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Production Deployment

### Option 1: Using Gunicorn (Recommended)

Gunicorn is a production-grade WSGI HTTP server for Python applications.

#### 1. Install Gunicorn

```bash
pip install gunicorn
```

#### 2. Set Production Environment Variables

```bash
export FLASK_DEBUG=false
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
export UPLOAD_FOLDER=/var/www/liturgia/uploads

# Create upload directory
sudo mkdir -p /var/www/liturgia/uploads
sudo chown $USER:$USER /var/www/liturgia/uploads
sudo chmod 755 /var/www/liturgia/uploads
```

#### 3. Run with Gunicorn

```bash
# Basic command
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With more options
gunicorn \
  --workers 4 \
  --bind 0.0.0.0:5000 \
  --access-logfile /var/log/liturgia/access.log \
  --error-logfile /var/log/liturgia/error.log \
  --log-level info \
  app:app
```

### Option 2: Using Systemd Service

Create a systemd service file for automatic startup.

#### 1. Create Service File

```bash
sudo nano /etc/systemd/system/liturgia.service
```

#### 2. Add Service Configuration

```ini
[Unit]
Description=Liturgia Católica Web Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/liturgia
Environment="PATH=/var/www/liturgia/venv/bin"
Environment="FLASK_DEBUG=false"
Environment="SECRET_KEY=your-production-secret-key-here"
Environment="UPLOAD_FOLDER=/var/www/liturgia/uploads"
ExecStart=/var/www/liturgia/venv/bin/gunicorn \
  --workers 4 \
  --bind 127.0.0.1:5000 \
  --access-logfile /var/log/liturgia/access.log \
  --error-logfile /var/log/liturgia/error.log \
  app:app

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable liturgia
sudo systemctl start liturgia
sudo systemctl status liturgia
```

### Option 3: Using Nginx as Reverse Proxy

Use Nginx to serve static files and proxy requests to Gunicorn.

#### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx
```

#### 2. Configure Nginx

Create `/etc/nginx/sites-available/liturgia`:

```nginx
server {
    listen 80;
    server_name liturgia.example.com;

    # Static files
    location /static {
        alias /var/www/liturgia/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
}
```

#### 3. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/liturgia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 4: Using Docker

Create a Docker container for easy deployment.

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create upload directory
RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# Set environment variables
ENV FLASK_DEBUG=false
ENV UPLOAD_FOLDER=/app/uploads

EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_DEBUG=false
      - SECRET_KEY=${SECRET_KEY}
      - UPLOAD_FOLDER=/app/uploads
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
```

#### 3. Build and Run

```bash
# Generate secret key
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f
```

## Environment Variables

### Required Variables

- `SECRET_KEY`: Secret key for Flask sessions (generate with `secrets.token_hex(32)`)

### Optional Variables

- `FLASK_DEBUG`: Enable/disable debug mode (default: `false`)
- `UPLOAD_FOLDER`: Directory for temporary PDF files (default: `/tmp/liturgia_pdfs`)

### Setting Environment Variables

#### Linux/Mac

```bash
# Temporary (current session)
export SECRET_KEY=your-secret-key
export FLASK_DEBUG=false

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export SECRET_KEY=your-secret-key' >> ~/.bashrc
echo 'export FLASK_DEBUG=false' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

```cmd
# Temporary (current session)
set SECRET_KEY=your-secret-key
set FLASK_DEBUG=false

# Permanent
setx SECRET_KEY "your-secret-key"
setx FLASK_DEBUG "false"
```

## Security Considerations

### 1. Secret Key

Always use a strong, randomly generated secret key in production:

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

### 2. Debug Mode

**NEVER** enable debug mode in production:

```bash
export FLASK_DEBUG=false
```

### 3. Upload Directory

Secure the upload directory:

```bash
sudo mkdir -p /var/www/liturgia/uploads
sudo chown www-data:www-data /var/www/liturgia/uploads
sudo chmod 755 /var/www/liturgia/uploads
```

### 4. HTTPS

Always use HTTPS in production. Use Let's Encrypt for free SSL certificates:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d liturgia.example.com
```

### 5. Firewall

Configure firewall to allow only necessary ports:

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 6. File Permissions

Set appropriate file permissions:

```bash
# Application files
sudo chown -R www-data:www-data /var/www/liturgia
sudo chmod -R 755 /var/www/liturgia

# Restrict sensitive files
sudo chmod 600 /var/www/liturgia/.env
```

## Troubleshooting

### Application Won't Start

1. Check if port 5000 is already in use:
   ```bash
   sudo lsof -i :5000
   ```

2. Check logs:
   ```bash
   # Gunicorn logs
   tail -f /var/log/liturgia/error.log
   
   # Systemd service logs
   sudo journalctl -u liturgia -f
   ```

### PDF Generation Fails

1. Check upload directory permissions:
   ```bash
   ls -la /var/www/liturgia/uploads
   ```

2. Check disk space:
   ```bash
   df -h
   ```

3. Install required dependencies:
   ```bash
   pip install reportlab
   ```

### Static Files Not Loading

1. Check Nginx configuration:
   ```bash
   sudo nginx -t
   ```

2. Verify static files path:
   ```bash
   ls -la /var/www/liturgia/static
   ```

3. Check Nginx logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

### Database Connection Issues

This application currently uses in-memory data structures. For persistent storage, you'll need to:

1. Add a database (PostgreSQL, MySQL, or SQLite)
2. Update models to use SQLAlchemy
3. Configure database connection string

## Monitoring

### Health Check Endpoint

Add a health check endpoint to monitor the application:

```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200
```

### Logging

Configure application logging:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        '/var/log/liturgia/app.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Liturgia startup')
```

## Backup and Maintenance

### Backup Strategy

1. **Application Files**: Keep in version control (Git)
2. **User Content**: Regular backups of upload directory
3. **Database**: Regular database dumps (when implemented)

### Maintenance Tasks

1. **Update Dependencies**:
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Clean Upload Directory**:
   ```bash
   # Remove files older than 7 days
   find /var/www/liturgia/uploads -type f -mtime +7 -delete
   ```

3. **Monitor Logs**:
   ```bash
   # Rotate logs
   sudo logrotate /etc/logrotate.d/liturgia
   ```

## Support

For issues and questions:
- GitHub Issues: https://github.com/josemaeldon/liturgia/issues
- Documentation: See README.md and WEB_README.md

## License

MIT License - See LICENSE file for details
