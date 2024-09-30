from django.contrib import admin
from .models import *

class CustomUser_Admin(admin.ModelAdmin):
    # Model = CustomUser
    list_display =["user", "task", "detail", "status", "date_created", "due_date", "complete_date"]
    readonly_fields = ["due_date", "complete_date"]
admin.site.register(Todo,CustomUser_Admin)
admin.site.register(CustomUser)
# admin.site.register(Todo)