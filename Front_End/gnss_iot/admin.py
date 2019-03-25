from django.contrib import admin

# Register your models here. 
from .models import DataGnss,Receiver

admin.site.register(DataGnss)
admin.site.register(Receiver)
