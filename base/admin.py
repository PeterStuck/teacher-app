from django.contrib import admin
from .models import Department, PresenceSymbol, SparedTime, LessonTopic, LessonCategory


@admin.register(Department)
class DepartmentAdminMeta(admin.ModelAdmin):
    list_display = ('full_name', 'name')
    list_per_page = 20


@admin.register(PresenceSymbol)
class PresenceSymbolAdminMeta(admin.ModelAdmin):
    list_display = ('full_name', 'symbol')
    list_per_page = 20


@admin.register(SparedTime)
class SparedTimeAdminMeta(admin.ModelAdmin):
    list_display = ('get_teacher_name', 'time')

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name()

    get_teacher_name.short_description = 'Teacher'


@admin.register(LessonTopic)
class LessonTopicAdminMeta(admin.ModelAdmin):
    list_display = ('topic', 'is_individual', 'get_teacher_name')

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name()

    get_teacher_name.short_description = 'Teacher'


@admin.register(LessonCategory)
class LessonCategoryAdminMeta(admin.ModelAdmin):
    verbose_name = 'Lesson categories'

