from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Employees)
admin.site.register(Levels)
admin.site.register(Hardware)
admin.site.register(Software)
admin.site.register(Processes)
admin.site.register(TaskHW)
admin.site.register(TaskSW)
admin.site.register(SkillsHW)
admin.site.register(SkillsSW)
admin.site.register(SkillsPR)