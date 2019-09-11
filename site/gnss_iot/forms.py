from django import forms

from .models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        device = Device
        fields = ['name']
        labels = {'name': ''}