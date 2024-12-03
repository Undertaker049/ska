from django.contrib import admin
from .models import *


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'get_department', 'role', 'get_subordinate_of')
    list_filter = ('role',)
    search_fields = ('name', 'department__name', 'user__username')
    list_per_page = 20
    ordering = ('name',)

    def get_department(self, obj):
        return obj.department if obj.role != 'admin' else '-'

    get_department.short_description = 'Отдел'

    def get_subordinate_of(self, obj):

        if obj.role == 'employee':
            return obj.subordinate_of

        return '-'

    get_subordinate_of.short_description = 'Руководитель'

    def get_fields(self, request, obj=None):
        fields = ['user', 'name', 'role']

        if not obj or obj.role != 'admin':
            fields.insert(2, 'department')

        if obj and obj.role == 'employee' or not obj:
            fields.append('subordinate_of')

        return fields

    def get_readonly_fields(self, request, obj=None):

        if obj and obj.role in ['supervisor', 'admin']:
            return ['subordinate_of']

        return []

    class Media:
        js = ('js/employees_admin.js',)

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