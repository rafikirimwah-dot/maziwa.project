from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsTruckAUser(permissions.BasePermission):
    """
    Allows access only to Truck A users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.username == 'truck_a'

class IsTruckBUser(permissions.BasePermission):
    """
    Allows access only to Truck B users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.username == 'truck_b'

class CanDeleteRecord(permissions.BasePermission):
    """
    Allows admin to delete any record, and truck users to delete their own.
    """
    def has_object_permission(self, request, view, obj):
        # Only staff users are allowed to delete records.
        return request.user.is_authenticated and request.user.is_staff

class CanEditRecord(permissions.BasePermission):
    """
    Allows admin to edit any record, and truck users to edit their own.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.recorded_by == request.user