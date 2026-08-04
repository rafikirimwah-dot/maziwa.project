from django import forms
from .models import MilkRecord

class MilkRecordForm(forms.ModelForm):
    class Meta:
        model = MilkRecord
        fields = [
            'farmer_name',
            'farmer_location',
            'milk_purity',
            'truck',
            # ============ NEW FIELDS ============
            'farmer_photo',
            'milk_certificate',
            'additional_notes',
        ]
        widgets = {
            'farmer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter farmer name'}),
            'farmer_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'milk_purity': forms.Select(attrs={'class': 'form-control'}),
            'truck': forms.Select(attrs={'class': 'form-control'}),
            # ============ NEW WIDGETS ============
            'farmer_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'milk_certificate': forms.FileInput(attrs={'class': 'form-control'}),
            'additional_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any additional notes...'
            }),
        }
        labels = {
            'farmer_name': 'Farmer Name',
            'farmer_location': 'Farmer Location',
            'milk_purity': 'Milk Purity Level',
            'truck': 'Collection Truck',
            'farmer_photo': 'Farmer Photo',
            'milk_certificate': 'Milk Certificate',
            'additional_notes': 'Additional Notes',
        }
        help_texts = {
            'farmer_photo': 'Upload a photo of the farmer (JPG, PNG, etc.)',
            'milk_certificate': 'Upload milk quality certificate (PDF, JPG, PNG)',
        }
