# fix_cors.py
import os
import sys

def fix_cors_settings():
    settings_path = 'maziwa/settings.py'
    
    if not os.path.exists(settings_path):
        print(f"Error: {settings_path} not found!")
        return
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Check if corsheaders is in INSTALLED_APPS
    if "'corsheaders'" not in content:
        print("Adding corsheaders to INSTALLED_APPS...")
        content = content.replace(
            "INSTALLED_APPS = [",
            "INSTALLED_APPS = [\n    'corsheaders',"
        )
    
    # Check if CorsMiddleware is in MIDDLEWARE
    if "corsheaders.middleware.CorsMiddleware" not in content:
        print("Adding CorsMiddleware to MIDDLEWARE...")
        content = content.replace(
            "MIDDLEWARE = [",
            "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',"
        )
    
    # Add CORS settings if not present
    if "CORS_ALLOW_ALL_ORIGINS" not in content:
        print("Adding CORS settings...")
        cors_settings = """
# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
"""
        # Add before the last line
        content = content.replace(
            "STATIC_URL = 'static/'",
            f"STATIC_URL = 'static/'\n{cors_settings}"
        )
    
    # Write the updated content
    with open(settings_path, 'w') as f:
        f.write(content)
    
    print("\n✅ CORS settings fixed!")
    print("\nPlease restart Django server:")
    print("  python manage.py runserver")
    print("\nAnd restart React:")
    print("  npm run dev")

if __name__ == "__main__":
    fix_cors_settings()