from django.contrib import admin
from .models import Department, PresenceSymbol


class DepartmentAdminMeta(admin.ModelAdmin):
    list_display = ('full_name', 'name')
    list_per_page = 20


admin.site.register(Department, DepartmentAdminMeta)


class PresenceSymbolAdminMeta(admin.ModelAdmin):
    list_display = ('full_name', 'symbol')
    list_per_page = 20


admin.site.register(PresenceSymbol, PresenceSymbolAdminMeta)