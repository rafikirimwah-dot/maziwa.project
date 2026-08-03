# create_users.py
from pathlib import Path
import sys
import os
import django

# Ensure project root is importable when executing this script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maziwa.settings')
django.setup()

from django.contrib.auth.models import User

def create_users():
    # Create or update superuser
    if User.objects.filter(username='cow').exists():
        user = User.objects.get(username='cow')
        user.email = 'cow@example.com'
        user.is_staff = True
        user.is_superuser = True
        user.set_password('oppo')
        user.save()
        print("✓ Superuser 'cow' already exists; password updated")
    elif User.objects.filter(username='admin').exists():
        user = User.objects.get(username='admin')
        user.username = 'cow'
        user.email = 'cow@example.com'
        user.is_staff = True
        user.is_superuser = True
        user.set_password('oppo')
        user.save()
        print("✓ Renamed existing admin user to 'cow' and updated password")
    else:
        User.objects.create_superuser(
            username='cow',
            email='cow@example.com',
            password='oppo'
        )
        print("✓ Superuser 'cow' created")
    
    # Create Truck A
    if not User.objects.filter(username='truck_a').exists():
        User.objects.create_user(
            username='truck_a',
            email='trucka@maziwa.com',
            password='truck123'
        )
        print("✓ Truck A user created")
    else:
        print("✓ Truck A user already exists")
    
    # Create Truck B
    if not User.objects.filter(username='truck_b').exists():
        User.objects.create_user(
            username='truck_b',
            email='truckb@maziwa.com',
            password='truck123'
        )
        print("✓ Truck B user created")
    else:
        print("✓ Truck B user already exists")
    
    # Display all users
    print("\n=== All Users in System ===")
    for user in User.objects.all():
        print(f"Username: {user.username}")
        print(f"  - Email: {user.email}")
        print(f"  - Staff: {user.is_staff}")
        print(f"  - Superuser: {user.is_superuser}")
        print(f"  - Active: {user.is_active}")
        print()

if __name__ == "__main__":
    create_users()