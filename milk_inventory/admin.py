from django.contrib import admin
from .models import MilkRecord

@admin.register(MilkRecord)
class MilkRecordAdmin(admin.ModelAdmin):
    list_display = ['farmer_name', 'farmer_location', 'milk_purity', 'truck', 'collection_time', 'recorded_by']
    list_filter = ['milk_purity', 'truck', 'collection_time']
    search_fields = ['farmer_name', 'farmer_location']
    date_hierarchy = 'collection_time'
    readonly_fields = ['created_at', 'updated_at']