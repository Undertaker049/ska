from django.contrib import admin
from .models import *


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_supervisor', 'subordinate_of')
    list_filter = ('department', 'is_supervisor')
    search_fields = ('name', 'department__name')
    list_per_page = 20
    ordering = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SkillsHW)
class SkillsHWAdmin(admin.ModelAdmin):
    list_display = ('employee', 'get_department', 'product', 'get_score')
    list_filter = ('employee__department', 'product')
    search_fields = ('employee__name', 'product__name')

    def get_department(self, obj):
        return obj.employee.department

    get_department.short_description = 'Отдел'
    get_department.admin_order_field = 'employee__department'

    def get_score(self, obj):
        return obj.get_score()

    get_score.short_description = 'Оценка'


@admin.register(SkillsSW)
class SkillsSWAdmin(admin.ModelAdmin):
    list_display = ('employee', 'get_department', 'product', 'get_score')
    list_filter = ('employee__department', 'product')
    search_fields = ('employee__name', 'product__name')

    def get_department(self, obj):
        return obj.employee.department

    get_department.short_description = 'Отдел'
    get_department.admin_order_field = 'employee__department'

    def get_score(self, obj):
        return obj.get_score()

    get_score.short_description = 'Оценка'


@admin.register(SkillsPR)
class SkillsPRAdmin(admin.ModelAdmin):
    list_display = ('employee', 'get_department', 'process', 'level')
    list_filter = ('employee__department', 'process')
    search_fields = ('employee__name', 'process__name')

    def get_department(self, obj):
        return obj.employee.department

    get_department.short_description = 'Отдел'
    get_department.admin_order_field = 'employee__department'

admin.site.register(Levels)
admin.site.register(Hardware)
admin.site.register(Software)
admin.site.register(Processes)
admin.site.register(TaskHW)
admin.site.register(TaskSW)