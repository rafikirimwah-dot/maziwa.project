from django.urls import path
from . import views
from .views import (
    MilkRecordListCreateView, 
    MilkRecordDetailView, 
    UserListView,
    CurrentUserView,
    dashboard_stats,
    api_root
)

app_name = 'milk_inventory'

urlpatterns = [
    # HTML Views
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_record, name='add_record'),
    path('edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('detail/<int:pk>/', views.record_detail, name='record_detail'),
    
    # REST API Endpoints
    path('api/', api_root, name='api_root'),
    path('api/milk-records/', MilkRecordListCreateView.as_view(), name='api_milk_records'),
    path('api/milk-records/<int:pk>/', MilkRecordDetailView.as_view(), name='api_milk_record_detail'),
    path('api/dashboard-stats/', dashboard_stats, name='api_dashboard_stats'),
    path('api/users/', UserListView.as_view(), name='api_users'),
    path('api/current-user/', CurrentUserView.as_view(), name='api_current_user'),
]