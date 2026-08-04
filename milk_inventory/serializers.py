from rest_framework import serializers
from .models import MilkRecord
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'role']
    
    def get_role(self, obj):
        if obj.is_superuser:
            return 'superuser'
        elif obj.is_staff:
            return 'admin'
        elif obj.username == 'truck_a':
            return 'truck_a'
        elif obj.username == 'truck_b':
            return 'truck_b'
        return 'user'

class MilkRecordSerializer(serializers.ModelSerializer):
    recorded_by_username = serializers.CharField(source='recorded_by.username', read_only=True)
    recorded_by_role = serializers.SerializerMethodField()
    purity_display = serializers.CharField(source='get_milk_purity_display', read_only=True)
    truck_display = serializers.CharField(source='get_truck_display', read_only=True)
    
    # ============ NEW: File URLs ============
    # These will return the full URL to access the files
    farmer_photo_url = serializers.SerializerMethodField()
    milk_certificate_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MilkRecord
        fields = [
            'id',
            'farmer_name',
            'farmer_location',
            'milk_purity',
            'purity_display',
            'truck',
            'truck_display',
            'collection_time',
            'recorded_by',
            'recorded_by_username',
            'recorded_by_role',
            # ============ NEW FIELDS ============
            'farmer_photo',
            'farmer_photo_url',      # Full URL for photo
            'milk_certificate',
            'milk_certificate_url',  # Full URL for certificate
            'additional_notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['recorded_by', 'created_at', 'updated_at']
    
    def get_recorded_by_role(self, obj):
        user = obj.recorded_by
        if user.is_superuser or user.is_staff:
            return 'admin'
        elif user.username == 'truck_a':
            return 'truck_a'
        elif user.username == 'truck_b':
            return 'truck_b'
        return 'user'
    
    # ============ NEW: Get File URLs ============
    def get_farmer_photo_url(self, obj):
        """Return the full URL for the farmer photo"""
        if obj.farmer_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.farmer_photo.url)
            return obj.farmer_photo.url
        return None
    
    def get_milk_certificate_url(self, obj):
        """Return the full URL for the milk certificate"""
        if obj.milk_certificate:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.milk_certificate.url)
            return obj.milk_certificate.url
        return None