import os, sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','maziwa.settings')
import django
django.setup()
from milk_inventory.models import MilkRecord

for r in MilkRecord.objects.all():
    print(r.id, r.farmer_name, r.truck, r.recorded_by.username, r.collection_time)
print('Total:', MilkRecord.objects.count())
