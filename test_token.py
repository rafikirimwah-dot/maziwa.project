import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","maziwa.settings")
import django
django.setup()
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
s = TokenObtainPairSerializer(data={"username":"admin","password":"admin123"})
try:
    ok = s.is_valid(raise_exception=True)
    print('OK', s.validated_data)
except Exception as e:
    import traceback
    traceback.print_exc()
