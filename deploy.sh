#!/bin/bash
# Full deployment script for HRC CRM Backend
# Run as root or with sudo on the Linux server
# Usage: bash deploy.sh

set -e

PROJECT_DIR="/var/www/hrc-crm-backend"
REPO_URL="your-git-repo-url-here"   # <-- replace with your actual repo URL
DOMAIN="crm.hrccosmos.com"
PYTHON="python3"

echo "==> Creating project directory..."
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/staticfiles
mkdir -p $PROJECT_DIR/media

echo "==> Cloning / pulling latest code..."
if [ -d "$PROJECT_DIR/.git" ]; then
    cd $PROJECT_DIR && git pull
else
    git clone $REPO_URL $PROJECT_DIR
fi

cd $PROJECT_DIR

echo "==> Setting up Python virtual environment..."
$PYTHON -m venv venv
source venv/bin/activate

echo "==> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Copying .env file (skip if already exists)..."
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp .env.example .env
    echo "  !! Edit $PROJECT_DIR/.env with your real values before continuing !!"
    exit 1
fi

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Setting permissions..."
chown -R www-data:www-data $PROJECT_DIR

echo "==> Installing Nginx config..."
cp nginx.conf /etc/nginx/sites-available/hrc-crm-backend
ln -sf /etc/nginx/sites-available/hrc-crm-backend /etc/nginx/sites-enabled/hrc-crm-backend
nginx -t && systemctl reload nginx

echo "==> Installing systemd service..."
cp hrc-crm-backend.service /etc/systemd/system/hrc-crm-backend.service
systemctl daemon-reload
systemctl enable hrc-crm-backend
systemctl restart hrc-crm-backend

echo "==> Obtaining SSL certificate via Certbot..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m admin@hrccosmos.com

echo ""
echo "==> Deployment complete! Service status:"
systemctl status hrc-crm-backend --no-pager
