import os, sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maziwa.settings')
import django
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

factory = APIRequestFactory()
request = factory.post('/api/token/', {'username':'truck_a','password':'truck123'}, format='json')
view = TokenObtainPairView.as_view()
try:
    response = view(request)
    print('STATUS', response.status_code)
    try:
        print(response.data)
    except Exception:
        print(response.rendered_content[:5000])
except Exception as e:
    print('EXCEPTION:', type(e).__name__, e)
    traceback.print_exc()
