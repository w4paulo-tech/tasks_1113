from django.contrib import admin as a
from .models import (CustomUser, Uzduotis, UzduotisInstance)
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(a.ModelAdmin):
    list_display = ['username', 'first_name', 'shift']
    fieldsets = (
        ('Custom Fields', {
            'fields': ['shift'],
            'classes': ['extrapretty']
        }),
        *UserAdmin.fieldsets,
    )
    ordering = ['shift']

class UzduotisAdmin(a.ModelAdmin):
    list_display = ['name', 'shift']
    ordering = ['shift']

class UzduotisInstanceAdmin(a.ModelAdmin):
    list_display = ['task', 'display_worker', 'status', 'due_date']

a.site.register(CustomUser, CustomUserAdmin)
a.site.register(Uzduotis, UzduotisAdmin)
a.site.register(UzduotisInstance, UzduotisInstanceAdmin)