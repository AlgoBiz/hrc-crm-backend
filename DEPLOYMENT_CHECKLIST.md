# Deployment Checklist for HRC CRM

## ✅ Changes Made (Ready to Deploy)

### 1. **Celery Integration**
- ✅ Added Celery configuration (`hrc_crm/celery.py`)
- ✅ Updated `__init__.py` to load Celery
- ✅ Created automated email reminder task (`user/tasks.py`)
- ✅ Added `django-celery-beat` for scheduled tasks

### 2. **Email System**
- ✅ Plan expiry reminder emails (30, 15, 2 days before expiry)
- ✅ Welcome emails for new customers
- ✅ Slot booking confirmation emails
- ✅ Email utility functions in `user/utils.py`

### 3. **Date Calculation Fix**
- ✅ Changed from month-based to day-based calculation
- ✅ 1 month = 30 days, 2 months = 60 days, etc.
- ✅ Consistent days_left calculation
- ✅ Applied to both create and update operations

### 4. **API Endpoints**
- ✅ Test email endpoint: `/api/test-email/`
- ✅ Trigger reminders endpoint: `/api/trigger-reminders/`

### 5. **Dependencies Updated**
- ✅ Added `celery==5.3.6`
- ✅ Added `django-celery-beat==2.5.0`
- ✅ Added `redis==5.0.1`
- ✅ Added `python-dateutil==2.8.2`

---

## 📋 Pre-Deployment Steps (Local)

### Step 1: Verify Local Environment
```bash
# Check if you're in the project directory
cd c:\Users\HANIMA\OneDrive\Desktop\new_project_algobiz\HRC_CRM

# Check Python version
python --version
```

### Step 2: Test Locally (Optional but Recommended)
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Test server
python manage.py runserver
```

### Step 3: Commit and Push Changes
```bash
# Check what files changed
git status

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Add Celery integration, email reminders, and day-based date calculation"

# Push to GitHub
git push origin main
```

---

## 🚀 Server Deployment Steps (EC2)

### Step 1: SSH into Server
```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

### Step 2: Navigate to Project
```bash
cd /var/www/hrc-crm-backend
```

### Step 3: Pull Latest Changes
```bash
git pull origin main
```

### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 5: Install New Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Install and Configure Redis
```bash
# Install Redis
sudo apt update
sudo apt install redis-server -y

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis

# Test Redis
redis-cli ping
# Should return: PONG
```

### Step 9: Restart Services
```bash
# Restart Django/Gunicorn
sudo systemctl restart hrc-crm-backend

# Check status
sudo systemctl status hrc-crm-backend
```

### Step 10: Start Celery Worker
```bash
# Create Celery systemd service file
sudo nano /etc/systemd/system/celery-worker.service
```

**Paste this content:**
```ini
[Unit]
Description=Celery Worker for HRC CRM
After=network.target redis.service

[Service]
Type=forking
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/hrc-crm-backend
Environment="PATH=/var/www/hrc-crm-backend/venv/bin"
ExecStart=/var/www/hrc-crm-backend/venv/bin/celery -A hrc_crm worker --loglevel=info --detach
ExecStop=/bin/kill -s TERM $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Save and enable:**
```bash
sudo systemctl daemon-reload
sudo systemctl start celery-worker
sudo systemctl enable celery-worker
sudo systemctl status celery-worker
```

### Step 11: Start Celery Beat (Scheduler)
```bash
# Create Celery Beat systemd service file
sudo nano /etc/systemd/system/celery-beat.service
```

**Paste this content:**
```ini
[Unit]
Description=Celery Beat Scheduler for HRC CRM
After=network.target redis.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/hrc-crm-backend
Environment="PATH=/var/www/hrc-crm-backend/venv/bin"
ExecStart=/var/www/hrc-crm-backend/venv/bin/celery -A hrc_crm beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Save and enable:**
```bash
sudo systemctl daemon-reload
sudo systemctl start celery-beat
sudo systemctl enable celery-beat
sudo systemctl status celery-beat
```

---

## 🧪 Testing on Server

### Test 1: Check Services
```bash
# Check Django
sudo systemctl status hrc-crm-backend

# Check Celery Worker
sudo systemctl status celery-worker

# Check Celery Beat
sudo systemctl status celery-beat

# Check Redis
sudo systemctl status redis
```

### Test 2: Test Email Sending
```bash
# SSH into server and run Django shell
python manage.py shell

# Test email
from user.models import Customer
from user.utils import send_plan_expiry_reminder

customer = Customer.objects.filter(email__isnull=False).first()
result = send_plan_expiry_reminder(customer, 30)
print("Success!" if result else "Failed!")
```

### Test 3: Test Celery Task
```bash
# In Django shell
from user.tasks import send_expiry_reminders
result = send_expiry_reminders.delay()
print(f"Task ID: {result.id}")
```

### Test 4: Check Logs
```bash
# Django logs
sudo journalctl -u hrc-crm-backend -f

# Celery Worker logs
sudo journalctl -u celery-worker -f

# Celery Beat logs
sudo journalctl -u celery-beat -f
```

---

## 📧 Configure Email Reminders Schedule

### Option 1: Using Django Admin
1. Go to: `https://crm.hrccosmos.com/admin/`
2. Navigate to: **Periodic Tasks** (from django-celery-beat)
3. Click **Add Periodic Task**
4. Configure:
   - **Name:** Send Plan Expiry Reminders
   - **Task:** `user.tasks.send_expiry_reminders`
   - **Interval:** Every 1 day
   - **Start Time:** 09:00 AM
   - **Enabled:** ✅

### Option 2: Using Django Shell
```python
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Create interval (every 1 day)
schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.DAYS,
)

# Create periodic task
PeriodicTask.objects.create(
    interval=schedule,
    name='Send Plan Expiry Reminders Daily',
    task='user.tasks.send_expiry_reminders',
)
```

---

## 🔧 Troubleshooting

### Issue: Celery worker not starting
```bash
# Check logs
sudo journalctl -u celery-worker -n 50

# Restart
sudo systemctl restart celery-worker
```

### Issue: Redis connection error
```bash
# Check Redis status
sudo systemctl status redis

# Test connection
redis-cli ping

# Restart Redis
sudo systemctl restart redis
```

### Issue: Email not sending
1. Check `.env` file has correct email credentials
2. For Gmail, use App Password (not regular password)
3. Check Django logs for email errors

### Issue: Tasks not running on schedule
```bash
# Check Celery Beat status
sudo systemctl status celery-beat

# Check scheduled tasks in Django admin
# Go to: /admin/django_celery_beat/periodictask/
```

---

## ✅ Deployment Complete!

After completing all steps:
- ✅ Django server running
- ✅ Celery worker running
- ✅ Celery beat scheduler running
- ✅ Redis running
- ✅ Email reminders scheduled
- ✅ All services auto-start on reboot

**Test the API:**
- Create a customer with a plan
- Check if `days_left` is calculated correctly
- Verify email sending works
