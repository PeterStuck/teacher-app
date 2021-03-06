from django.contrib import admin
from .models import Department, PresenceSymbol, SparedTime


class DepartmentAdminMeta(admin.ModelAdmin):
    list_display = ('full_name', 'name')
    list_per_page = 20


admin.site.register(Department, DepartmentAdminMeta)


class PresenceSymbolAdminMeta(admin.ModelAdmin):
    list_display = ('full_name', 'symbol')
    list_per_page = 20


admin.site.register(PresenceSymbol, PresenceSymbolAdminMeta)


class SparedTimeAdminMeta(admin.ModelAdmin):
    list_display = ('get_teacher_name', 'time')

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name()

    get_teacher_name.short_description = 'Teacher'


admin.site.register(SparedTime, SparedTimeAdminMeta)