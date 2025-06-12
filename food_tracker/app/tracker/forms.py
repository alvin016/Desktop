# forms.py 只保留這個
from django import forms
from .models import FoodRecord,WeightRecord

class FoodRecordForm(forms.ModelForm):
    class Meta:
        model = FoodRecord
        fields = ['date', 'category', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class WeightRecordForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }