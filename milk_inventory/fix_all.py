# fix_all.py
import os
import sys

def fix_urls():
    # Fix main urls.py
    url_content = '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('milk_inventory.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    with open('maziwa/urls.py', 'w') as f:
        f.write(url_content)
    print("✓ Fixed main urls.py")
    
    # Fix milk_inventory urls.py
    inventory_urls = '''from django.urls import path
from . import views

app_name = 'milk_inventory'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_record, name='add_record'),
    path('edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('detail/<int:pk>/', views.record_detail, name='record_detail'),
]
'''
    
    os.makedirs('milk_inventory', exist_ok=True)
    with open('milk_inventory/urls.py', 'w') as f:
        f.write(inventory_urls)
    print("✓ Fixed milk_inventory/urls.py")
    
    # Fix accounts urls.py
    accounts_urls = '''from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
'''
    
    os.makedirs('accounts', exist_ok=True)
    with open('accounts/urls.py', 'w') as f:
        f.write(accounts_urls)
    print("✓ Fixed accounts/urls.py")

if __name__ == "__main__":
    fix_urls()
    print("\n✅ All URL files fixed!")
    print("Now run:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
    print("4. python manage.py runserver")