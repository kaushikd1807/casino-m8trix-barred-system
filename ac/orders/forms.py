from django import forms
from .models import Order, Document
from django.forms import ClearableFileInput


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
