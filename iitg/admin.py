from django.contrib import admin

# Register your models here.

from .models import Event,Student,Admin,Page

admin.site.register(Event)
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Page)
