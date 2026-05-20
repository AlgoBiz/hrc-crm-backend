# Quick Guide: Push Changes to Server

## 🎯 What We Changed

1. ✅ **Celery Integration** - Automated background tasks
2. ✅ **Email Reminders** - Automatic plan expiry notifications
3. ✅ **Day-Based Calculation** - Fixed date calculation (1 month = 30 days)
4. ✅ **Updated Dependencies** - Added Celery, Redis, django-celery-beat

---

## 📤 Step 1: Push from Local (Windows)

Open Git Bash or Command Prompt in your project folder:

```bash
# Navigate to project
cd c:\Users\HANIMA\OneDrive\Desktop\new_project_algobiz\HRC_CRM

# Check what changed
git status

# Add all changes
git add .

# Commit
git commit -m "Add Celery, email reminders, and day-based date calculation"

# Push to GitHub
git push origin main
```

**If you get an error about branch name, try:**
```bash
git push origin master
```

---

## 🖥️ Step 2: Deploy on Server (EC2)

### A. Connect to Server
```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

### B. Pull Latest Code
```bash
cd /var/www/hrc-crm-backend
git pull origin main
```

### C. Run Deployment Script
```bash
# Make script executable
chmod +x deploy_to_server.sh

# Run deployment
./deploy_to_server.sh
```

**OR do it manually:**
```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart hrc-crm-backend
```

---

## 🔧 Step 3: Install Redis (First Time Only)

```bash
# Install Redis
sudo apt update
sudo apt install redis-server -y

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis

# Test
redis-cli ping
# Should return: PONG
```

---

## 🔄 Step 4: Setup Celery Services (First Time Only)

### Create Celery Worker Service
```bash
sudo nano /etc/systemd/system/celery-worker.service
```

Paste this:
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

Save: `Ctrl+X`, then `Y`, then `Enter`

### Create Celery Beat Service
```bash
sudo nano /etc/systemd/system/celery-beat.service
```

Paste this:
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

Save: `Ctrl+X`, then `Y`, then `Enter`

### Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl start celery-worker
sudo systemctl enable celery-worker
sudo systemctl start celery-beat
sudo systemctl enable celery-beat
```

---

## ✅ Step 5: Verify Everything Works

### Check Services
```bash
sudo systemctl status hrc-crm-backend
sudo systemctl status celery-worker
sudo systemctl status celery-beat
sudo systemctl status redis
```

All should show: **active (running)** in green

### Test Email Sending
```bash
python manage.py shell
```

Then in Python shell:
```python
from user.models import Customer
from user.utils import send_plan_expiry_reminder

customer = Customer.objects.filter(email__isnull=False).first()
if customer:
    result = send_plan_expiry_reminder(customer, 30)
    print("✅ Success!" if result else "❌ Failed!")
```

### Test Celery Task
```python
from user.tasks import send_expiry_reminders
result = send_expiry_reminders.delay()
print(f"Task ID: {result.id}")
```

Exit shell: `exit()`

---

## 📧 Step 6: Schedule Daily Email Reminders

### Option 1: Django Admin (Easiest)
1. Go to: `https://crm.hrccosmos.com/admin/`
2. Login as superuser
3. Find: **Periodic Tasks** (under DJANGO CELERY BEAT)
4. Click: **Add Periodic Task**
5. Fill in:
   - **Name:** Send Plan Expiry Reminders
   - **Task (registered):** `user.tasks.send_expiry_reminders`
   - **Interval:** Click the green + to create new
     - **Every:** 1
     - **Period:** Days
     - Save
   - **Start Datetime:** Leave blank (starts immediately)
   - **Enabled:** ✅ Check this
6. Click **Save**

### Option 2: Django Shell
```bash
python manage.py shell
```

```python
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Create daily schedule
schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.DAYS,
)

# Create task
PeriodicTask.objects.create(
    interval=schedule,
    name='Send Plan Expiry Reminders Daily',
    task='user.tasks.send_expiry_reminders',
    enabled=True,
)

print("✅ Scheduled task created!")
```

---

## 🎉 Done!

Your server now has:
- ✅ Latest code with day-based date calculation
- ✅ Celery for background tasks
- ✅ Automated email reminders (30, 15, 2 days before expiry)
- ✅ All services running and auto-start on reboot

---

## 🔍 Useful Commands

### View Logs
```bash
# Django logs
sudo journalctl -u hrc-crm-backend -f

# Celery Worker logs
sudo journalctl -u celery-worker -f

# Celery Beat logs
sudo journalctl -u celery-beat -f
```

### Restart Services
```bash
sudo systemctl restart hrc-crm-backend
sudo systemctl restart celery-worker
sudo systemctl restart celery-beat
```

### Check Service Status
```bash
sudo systemctl status hrc-crm-backend
sudo systemctl status celery-worker
sudo systemctl status celery-beat
sudo systemctl status redis
```

---

## ⚠️ Troubleshooting

### If Celery Worker fails:
```bash
# Check logs
sudo journalctl -u celery-worker -n 50

# Try running manually to see errors
cd /var/www/hrc-crm-backend
source venv/bin/activate
celery -A hrc_crm worker --loglevel=info
```

### If emails not sending:
1. Check `.env` file has correct email settings
2. For Gmail, use App Password (not regular password)
3. Check logs: `sudo journalctl -u celery-worker -f`

### If Redis not working:
```bash
sudo systemctl restart redis
redis-cli ping  # Should return PONG
```

---

## 📞 Need Help?

Check the detailed guide: `DEPLOYMENT_CHECKLIST.md`
