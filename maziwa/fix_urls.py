# fix_urls.py
import os
import sys

def fix_project_urls():
    url_file = 'maziwa/urls.py'
    
    if os.path.exists(url_file):
        with open(url_file, 'r') as f:
            content = f.read()
        
        # Check if URLs are correct
        if 'gumbaru_core' in content:
            print("Found wrong project name in URLs. Fixing...")
            
            # Backup the file
            with open(url_file + '.backup', 'w') as f:
                f.write(content)
            
            # Correct content
            correct_content = '''from django.contrib import admin
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
            
            with open(url_file, 'w') as f:
                f.write(correct_content)
            
            print("✓ URLs fixed successfully!")
        else:
            print("URLs look correct.")
    else:
        print(f"Error: {url_file} not found!")

if __name__ == "__main__":
    fix_project_urls()