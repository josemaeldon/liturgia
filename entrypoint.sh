#!/bin/bash
# Entrypoint script for Liturgia Docker container
# Initializes database and starts Apache

set -e

echo "========================================="
echo "  Liturgia - Starting Container"
echo "========================================="

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if python3 -c "
import psycopg2
import os
import sys
try:
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        port=os.environ.get('DB_PORT', '5432'),
        dbname=os.environ.get('DB_DATABASE', 'liturgia_db'),
        user=os.environ.get('DB_USERNAME', 'postgres'),
        password=os.environ.get('DB_PASSWORD', ''),
        connect_timeout=3
    )
    conn.close()
    sys.exit(0)
except:
    sys.exit(1)
" 2>/dev/null; then
        echo "PostgreSQL is ready!"
        break
    fi
    
    attempt=$((attempt + 1))
    echo "  Attempt $attempt/$max_attempts - waiting for PostgreSQL..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "ERROR: PostgreSQL did not become ready in time"
    exit 1
fi

# Initialize/upgrade database
echo ""
echo "Initializing database..."
cd /var/www
python3 init_db.py

if [ $? -eq 0 ]; then
    echo "Database initialized successfully!"
else
    echo "WARNING: Database initialization had errors, but continuing..."
fi

# Start Apache
echo ""
echo "Starting Apache..."
echo "========================================="
exec /usr/sbin/apache2ctl -D FOREGROUND
