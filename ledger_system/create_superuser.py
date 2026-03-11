from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ledger_system.settings")
django.setup()

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "kirti")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Scale@55")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)