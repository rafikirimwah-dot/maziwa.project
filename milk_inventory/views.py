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

# ============ API VIEWS ============

class MilkRecordListCreateView(generics.ListCreateAPIView):
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
        serializer.save(recorded_by=self.request.user)

class MilkRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
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
        return render(request, 'milk_inventory/dashboard.html')
    except Exception as e:
        return HttpResponse(f'Dashboard - Error: {str(e)}', status=200)

def add_record(request):
    if request.method == 'POST':
        form = MilkRecordForm(request.POST)
        if form.is_valid():
            form.save()
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
        form = MilkRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('milk_inventory:dashboard')
    else:
        form = MilkRecordForm(instance=record)
    try:
        return render(request, 'milk_inventory/add_record.html', {'form': form, 'edit': True})
    except Exception as e:
        return HttpResponse(f'Edit record - Error: {str(e)}')

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