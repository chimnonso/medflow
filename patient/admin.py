from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Inventory)
admin.site.register(Prescription)