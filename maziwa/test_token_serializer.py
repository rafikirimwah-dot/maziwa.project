import os
import django
import traceback
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maziwa.settings')
django.setup()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

creds = {'username': 'truck_a', 'password': 'truck123'}
try:
    serializer = TokenObtainPairSerializer(data=creds)
    valid = serializer.is_valid(raise_exception=True)
    print('VALID:', valid)
    print(serializer.validated_data)
except Exception as e:
    print('EXCEPTION:', type(e).__name__, str(e))
    traceback.print_exc()
