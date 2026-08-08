from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from .models import MilkRecord
from .serializers import MilkRecordSerializer, UserSerializer
from .permissions import CanDeleteRecord, CanEditRecord, IsAdminUser as CustomIsAdminUser
from .forms import MilkRecordForm
import os
from django.conf import settings

# Pillow for server-side watermarking
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None

# ============ API VIEWS (Already Updated) ============

class MilkRecordListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating milk records with file uploads.
    """
    serializer_class = MilkRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['milk_purity', 'truck', 'farmer_name']
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return MilkRecord.objects.none()
            
        if user.is_staff or user.is_superuser:
            return MilkRecord.objects.all()
        elif user.username == 'truck_a':
            return MilkRecord.objects.filter(truck='TRUCK_A')
        elif user.username == 'truck_b':
            return MilkRecord.objects.filter(truck='TRUCK_B')
        return MilkRecord.objects.none()
    
    def perform_create(self, serializer):
        """
        Save the record with the current user as recorded_by.
        File uploads are handled automatically by DRF.
        """
        serializer.save(recorded_by=self.request.user)

class MilkRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting records with file uploads.
    """
    serializer_class = MilkRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return MilkRecord.objects.none()
            
        if user.is_staff or user.is_superuser:
            return MilkRecord.objects.all()
        elif user.username == 'truck_a':
            return MilkRecord.objects.filter(truck='TRUCK_A')
        elif user.username == 'truck_b':
            return MilkRecord.objects.filter(truck='TRUCK_B')
        return MilkRecord.objects.none()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), CanEditRecord()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), CanDeleteRecord()]
        return [IsAuthenticated()]
    
    def perform_update(self, serializer):
        """
        Handle file updates. The serializer will handle the file fields.
        """
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Delete the record and optionally delete associated files.
        """
        # Optionally delete files when record is deleted
        # This prevents orphaned files
        if instance.farmer_photo:
            instance.farmer_photo.delete(save=False)
        if instance.milk_certificate:
            instance.milk_certificate.delete(save=False)
        instance.delete()

# ... rest of your views ...

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [CustomIsAdminUser]

    def get_queryset(self):
        # Only exclude users that exist
        try:
            demo_usernames = ['admin', 'truck_a', 'truck_b']
            return User.objects.exclude(username__in=demo_usernames)
        except:
            return User.objects.all()

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# ============ CUSTOM ENDPOINTS ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)
        
    if user.is_staff or user.is_superuser:
        records = MilkRecord.objects.all()
        user_type = 'admin'
    elif user.username == 'truck_a':
        records = MilkRecord.objects.filter(truck='TRUCK_A')
        user_type = 'truck_a'
    elif user.username == 'truck_b':
        records = MilkRecord.objects.filter(truck='TRUCK_B')
        user_type = 'truck_b'
    else:
        records = MilkRecord.objects.none()
        user_type = 'user'
    
    return Response({
        'total_records': records.count(),
        'purity_stats': records.values('milk_purity').annotate(count=Count('milk_purity')),
        'user_type': user_type,
        'username': user.username,
        'is_admin': user.is_staff or user.is_superuser
    })

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Welcome to MAZIWA Milk Inventory API',
        'endpoints': {
            'milk_records': '/api/milk-records/',
            'current_user': '/api/current-user/',
            'dashboard_stats': '/api/dashboard-stats/',
        }
    })

# ============ HTML Views ============

def dashboard(request):
    try:
        user = request.user
        if user.is_staff or user.is_superuser:
            records = MilkRecord.objects.all()
        elif user.username == 'truck_a':
            records = MilkRecord.objects.filter(truck='TRUCK_A')
        elif user.username == 'truck_b':
            records = MilkRecord.objects.filter(truck='TRUCK_B')
        else:
            records = MilkRecord.objects.filter(recorded_by=user)

        purity_stats = records.values('milk_purity').annotate(count=Count('milk_purity'))
        return render(request, 'milk_inventory/dashboard.html', {
            'records': records,
            'total_records': records.count(),
            'purity_stats': purity_stats,
        })
    except Exception as e:
        return HttpResponse(f'Dashboard - Error: {str(e)}', status=200)


def add_record(request):
    if request.method == 'POST':
        form = MilkRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save()
            # Process uploaded certificate to bake watermark if it's an image
            try:
                if Image and record.milk_certificate:
                    cert_path = record.milk_certificate.path
                    _apply_image_watermark(cert_path, text='maziwa fresh since 98')
            except Exception:
                pass
            return redirect('milk_inventory:dashboard')
    else:
        form = MilkRecordForm()
    try:
        return render(request, 'milk_inventory/add_record.html', {'form': form})
    except Exception as e:
        return HttpResponse(f'Add record - Error: {str(e)}')

def edit_record(request, pk):
    record = get_object_or_404(MilkRecord, pk=pk)
    if request.method == 'POST':
        form = MilkRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            record = form.save()
            # If a new certificate was uploaded, re-apply watermark
            try:
                if Image and 'milk_certificate' in request.FILES and record.milk_certificate:
                    cert_path = record.milk_certificate.path
                    _apply_image_watermark(cert_path, text='maziwa fresh since 98')
            except Exception:
                pass
            return redirect('milk_inventory:dashboard')
    else:
        form = MilkRecordForm(instance=record)
    try:
        return render(request, 'milk_inventory/add_record.html', {'form': form, 'edit': True})
    except Exception as e:
        return HttpResponse(f'Edit record - Error: {str(e)}')


def farmer_images(request, pk):
    """Gallery view showing uploaded images for a specific farmer."""
    record = get_object_or_404(MilkRecord, pk=pk)
    records = MilkRecord.objects.filter(farmer_name=record.farmer_name)
    return render(request, 'milk_inventory/farmer_images.html', {
        'records': records,
        'farmer_name': record.farmer_name
    })


def _apply_image_watermark(image_path, text='maziwa fresh since 98'): 
    """Apply a semi-transparent rotated watermark text to an image file in-place.

    This function attempts to open the image at image_path, draw the watermark,
    and overwrite the original file. Non-image files are ignored by caller.
    """
    if not Image:
        return
    if not os.path.exists(image_path):
        return

    try:
        with Image.open(image_path) as im:
            fmt = im.format
            im = im.convert('RGBA')

            width, height = im.size

            # Create watermark image
            watermark = Image.new('RGBA', im.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark)

            # Choose font size relative to image width
            font_size = max(20, int(width / 10))
            font = None
            try:
                # Try common Windows font path
                font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arial.ttf')
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.truetype('arial.ttf', font_size)
            except Exception:
                try:
                    font = ImageFont.load_default()
                except Exception:
                    font = None

            text_width, text_height = draw.textsize(text, font=font)

            # Position at center
            x = (width - text_width) / 2
            y = (height - text_height) / 2

            # Draw text with semi-transparent white
            draw.text((x, y), text, fill=(255, 255, 255, 80), font=font)

            # Rotate watermark slightly
            watermark = watermark.rotate(-20, expand=1)

            # Composite watermark onto original image
            combined = Image.alpha_composite(im, watermark.crop((0, 0, width, height)))

            # Save back to same path
            if fmt and fmt.upper() in ['JPEG', 'JPG']:
                rgb = combined.convert('RGB')
                rgb.save(image_path, format='JPEG', quality=85)
            else:
                combined.save(image_path, format=fmt)
    except Exception:
        return

def delete_record(request, pk):
    record = get_object_or_404(MilkRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('milk_inventory:dashboard')
    try:
        return render(request, 'milk_inventory/delete_record.html', {'record': record})
    except Exception as e:
        return HttpResponse(f'Delete record - Error: {str(e)}')

def record_detail(request, pk):
    record = get_object_or_404(MilkRecord, pk=pk)
    try:
        return render(request, 'milk_inventory/detail.html', {'record': record})
    except Exception as e:
        return HttpResponse(f'Record detail - Error: {str(e)}')