from django.contrib import admin

# Register your models here.

from .models import Event,Student,Admin

admin.site.register(Event)
admin.site.register(Student)
admin.site.register(Admin)
