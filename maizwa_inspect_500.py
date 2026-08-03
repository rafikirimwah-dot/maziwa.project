import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path('.').resolve()))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maziwa.settings')
django.setup()

from django.test import Client
import re

c = Client()
resp = c.post('/api/token/', data='{"username":"truck_a","password":"truck123"}', content_type='application/json')
print('STATUS:', resp.status_code)
text = resp.content.decode('utf-8', errors='ignore')
if resp.status_code == 500:
    m = re.search(r'(Exception Type:.*?)(Exception Value:.*?)(</pre>)', text, re.S)
    if m:
        print('\n--- Exception Info ---\n')
        print(m.group(1))
        print(m.group(2))
    else:
        # fallback: print first 4000 chars
        print(text[:4000])
else:
    print(text)
