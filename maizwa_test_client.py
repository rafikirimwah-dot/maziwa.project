import os
import django
from pathlib import Path
import sys

sys.path.insert(0, str(Path('.').resolve()))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maziwa.settings')
django.setup()

from django.test import Client

c = Client()
resp = c.post('/api/token/', data='{"username":"truck_a","password":"truck123"}', content_type='application/json')
print('STATUS:', resp.status_code)
print('CONTENT:\n', resp.content.decode('utf-8'))
