from django.contrib import admin

from .models import RevalidationStudent, IndividualLessonPaymentType


class RevalidationStudentAdminMeta(admin.ModelAdmin):
    list_display = ('name', 'get_department_name', 'get_teacher_name')

    def get_department_name(self, obj):
        return obj.department.full_name

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name()

    get_department_name.short_description = 'Department'
    get_teacher_name.short_description = 'Teacher'


admin.site.register(RevalidationStudent, RevalidationStudentAdminMeta)
admin.site.register(IndividualLessonPaymentType)
