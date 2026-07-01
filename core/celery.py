import os
from celery import Celery

# from accounts.tasks import send_email

# تنظیم Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# خواندن تنظیمات از Django settings با prefix CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# پیدا کردن taskها به صورت خودکار از فایل‌های tasks.py
app.autodiscover_tasks()

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, send_email.s(), name='send email  every 10s')
