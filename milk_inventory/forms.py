from django import forms
from .models import MilkRecord

class MilkRecordForm(forms.ModelForm):
    collection_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        }),
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Collection Time',
    )

    class Meta:
        model = MilkRecord
        fields = ['farmer_name', 'farmer_location', 'collection_time', 'milk_purity', 'truck']
        widgets = {
            'farmer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter farmer name'}),
            'farmer_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'milk_purity': forms.Select(attrs={'class': 'form-control'}),
            'truck': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'farmer_name': 'Farmer Name',
            'farmer_location': 'Farmer Location',
            'milk_purity': 'Milk Purity Level',
            'truck': 'Collection Truck',
        }
