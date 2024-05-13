from django.db import models


# Create your models here.
class Employees(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Levels(models.Model):
    weight = models.IntegerField(unique=True)
    level = models.TextField(unique=True)
    description = models.TextField(unique=True)


class Hardware(models.Model):
    product = models.TextField(unique=True)


class Software(models.Model):
    product = models.TextField(unique=True)


class Processes(models.Model):
    process = models.TextField(unique=True)


class TaskHW(models.Model):
    task = models.TextField(unique=True)


class TaskSW(models.Model):
    task = models.TextField(unique=True)


class SkillsHW(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    product = models.ForeignKey(Hardware, on_delete=models.DO_NOTHING, to_field="product")
    task = models.ForeignKey(TaskHW, on_delete=models.DO_NOTHING, to_field="task")
    level = models.ForeignKey(Levels, on_delete=models.DO_NOTHING, to_field="level")
    time = models.DateTimeField(auto_now_add=True)


class SkillsSW(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    product = models.ForeignKey(Software, on_delete=models.DO_NOTHING, to_field="product")
    task = models.ForeignKey(TaskSW, on_delete=models.DO_NOTHING, to_field="task")
    level = models.ForeignKey(Levels, on_delete=models.DO_NOTHING, to_field="level")
    time = models.DateTimeField(auto_now_add=True)


class SKillsPr(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    process = models.ForeignKey(Processes, on_delete=models.DO_NOTHING, to_field="process")
    level = models.ForeignKey(Levels, on_delete=models.DO_NOTHING, to_field="level")
    time = models.DateTimeField(auto_now_add=True)
