import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maziwa.settings')

django.setup()

from django.contrib.auth.models import User

for u in User.objects.all():
    print(f"id={u.id}\tusername={u.username}\tstaff={u.is_staff}\tsuperuser={u.is_superuser}\tpassword_hash={u.password}")
