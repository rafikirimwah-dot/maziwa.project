import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maziwa.settings')
import django
django.setup()
from django.test import Client
import json
c = Client()
resp = c.post('/api/token/', data=json.dumps({'username':'admin','password':'admin123'}), content_type='application/json')
print('STATUS', resp.status_code)
print(resp.content.decode())
