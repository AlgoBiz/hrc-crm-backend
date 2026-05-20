#!/bin/bash

# HRC CRM Deployment Script
# Run this on the EC2 server after pulling latest code

echo "🚀 Starting HRC CRM Deployment..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="/var/www/hrc-crm-backend"

# Navigate to project
cd $PROJECT_DIR || exit

echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -r requirements.txt

echo -e "${YELLOW}🗄️  Running migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

echo -e "${YELLOW}📁 Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${YELLOW}🔄 Restarting services...${NC}"

# Restart Django/Gunicorn
sudo systemctl restart hrc-crm-backend
echo -e "${GREEN}✅ Django restarted${NC}"

# Restart Celery Worker
if systemctl is-active --quiet celery-worker; then
    sudo systemctl restart celery-worker
    echo -e "${GREEN}✅ Celery Worker restarted${NC}"
else
    echo -e "${RED}⚠️  Celery Worker not running. Start it manually.${NC}"
fi

# Restart Celery Beat
if systemctl is-active --quiet celery-beat; then
    sudo systemctl restart celery-beat
    echo -e "${GREEN}✅ Celery Beat restarted${NC}"
else
    echo -e "${RED}⚠️  Celery Beat not running. Start it manually.${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo "📊 Service Status:"
echo "===================="
sudo systemctl status hrc-crm-backend --no-pager | grep "Active:"
sudo systemctl status celery-worker --no-pager | grep "Active:" 2>/dev/null || echo "Celery Worker: Not configured"
sudo systemctl status celery-beat --no-pager | grep "Active:" 2>/dev/null || echo "Celery Beat: Not configured"
sudo systemctl status redis --no-pager | grep "Active:" 2>/dev/null || echo "Redis: Not configured"

echo ""
echo "📝 View logs with:"
echo "  Django:        sudo journalctl -u hrc-crm-backend -f"
echo "  Celery Worker: sudo journalctl -u celery-worker -f"
echo "  Celery Beat:   sudo journalctl -u celery-beat -f"
