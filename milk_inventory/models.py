from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MilkRecord(models.Model):
    # Milk purity levels
    PURITY_CHOICES = [
        ('LOW', 'Low'),
        ('MID', 'Medium'),
        ('GREAT', 'Great'),
    ]
    
    # Truck choices
    TRUCK_CHOICES = [
        ('TRUCK_A', 'Truck A'),
        ('TRUCK_B', 'Truck B'),
    ]
    
    farmer_name = models.CharField(max_length=100)
    farmer_location = models.CharField(max_length=200)
    milk_purity = models.CharField(max_length=5, choices=PURITY_CHOICES)
    truck = models.CharField(max_length=10, choices=TRUCK_CHOICES)
    collection_time = models.DateTimeField(default=timezone.now)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # ============ NEW MEDIA FIELDS ============
    # Farmer profile photo - ImageField for photos
    farmer_photo = models.ImageField(
        upload_to='farmer_photos/',  # Subfolder within media
        blank=True,                  # Optional field
        null=True,                   # Can be null in database
        help_text='Upload a photo of the farmer'
    )
    
    # Milk quality certificate - FileField for any document
    milk_certificate = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True,
        help_text='Upload milk quality certificate (PDF, JPG, PNG)'
    )
    
    # Additional notes/document - Text field for extra info
    additional_notes = models.TextField(
        blank=True,
        null=True,
        help_text='Any additional notes about this milk collection'
    )
    
    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farmer_name} - {self.truck} - {self.get_milk_purity_display()}"
    
    class Meta:
        ordering = ['-collection_time']