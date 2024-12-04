from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
        ordering = ['name']


class Employees(models.Model):

    # Связь с пользователем - обязательное поле
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name="Пользователь",
        null=False,
        blank=False
    )

    # ФИО сотрудника - обязательное поле
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ФИО",
        null=False,
        blank=False
    )

    # Отдел сотрудника - может быть пустым только для администраторов
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name="Отдел"
    )

    # Руководитель - может быть пустым для руководителей и администраторов
    subordinate_of = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None,
        verbose_name="Руководитель"
    )

    # Роль - обязательное поле
    role = models.CharField(
        max_length=20,
        choices=[
            ('employee', 'Сотрудник'),
            ('supervisor', 'Руководитель'),
            ('admin', 'Администратор')
        ],
        default='employee',
        verbose_name="Роль",
        null=False,
        blank=False
    )

    # Валидация данных модели
    def clean(self):
        super().clean()

        if self.role in ['supervisor', 'admin'] and self.subordinate_of:
            self.subordinate_of = None

        if self.role == 'admin':
            self.department = None

        elif not self.department:
            raise ValidationError({'department': 'This field is required.'})

    # Переопределение метода сохранения для автоматической валидации данных
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        if self.name and ' ' in self.name:
            first_name, last_name = self.name.split(' ', 1)
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.save()

    def __str__(self):
        return f"{self.name} ({self.department})" if self.department else self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['name'] # Сортировка по умолчанию по ФИО


class Levels(models.Model):
    weight = models.IntegerField(unique=True, verbose_name="Вес")
    level = models.TextField(unique=True, verbose_name="Уровень")
    description = models.TextField(unique=True, verbose_name="Описание")

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"
        ordering = ['weight']


class Hardware(models.Model):
    product = models.TextField(unique=True, verbose_name="Продукт")

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ['product']


class Software(models.Model):
    product = models.TextField(unique=True, verbose_name="Продукт")

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "ПО"
        verbose_name_plural = "ПО"
        ordering = ['product']


class Processes(models.Model):
    process = models.TextField(unique=True, verbose_name="Процесс")

    def __str__(self):
        return self.process

    class Meta:
        verbose_name = "Процесс"
        verbose_name_plural = "Процессы"
        ordering = ['process']


class TaskHW(models.Model):
    task = models.TextField(unique=True, verbose_name="Задача")

    def __str__(self):
        return self.task

    class Meta:
        verbose_name = "Задача по оборудованию"
        verbose_name_plural = "Задачи по оборудованию"
        ordering = ['task']


class TaskSW(models.Model):
    task = models.TextField(unique=True, verbose_name="Задача")

    def __str__(self):
        return self.task

    class Meta:
        verbose_name = "Задача по ПО"
        verbose_name_plural = "Задачи по ПО"
        ordering = ['task']


class SkillsHW(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, verbose_name="Сотрудник")
    product = models.ForeignKey(Hardware, on_delete=models.DO_NOTHING, to_field="product", verbose_name="Продукт")
    task = models.ForeignKey(TaskHW, on_delete=models.DO_NOTHING, to_field="task", verbose_name="Задача")
    level = models.ForeignKey(Levels, on_delete=models.DO_NOTHING, to_field="level", verbose_name="Уровень")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время оценки")

    def get_score(self):
        return self.level.weight if self.level else 0

    def __str__(self):
        return f"{self.employee} - {self.product} ({self.level})"

    class Meta:
        verbose_name = "Навык по оборудованию"
        verbose_name_plural = "Навыки по оборудованию"
        ordering = ['-time']


class SkillsSW(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, verbose_name="Сотрудник")
    product = models.ForeignKey(Software, on_delete=models.DO_NOTHING, to_field="product", verbose_name="Продукт")
    task = models.ForeignKey(TaskSW, on_delete=models.DO_NOTHING, to_field="task", verbose_name="Задача")
    level = models.ForeignKey(Levels, on_delete=models.DO_NOTHING, to_field="level", verbose_name="Уровень")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время оценки")

    def get_score(self):
        return self.level.weight if self.level else 0

    def __str__(self):
        return f"{self.employee} - {self.product} ({self.level})"

    class Meta:
        verbose_name = "Навык по ПО"
        verbose_name_plural = "Навыки по ПО"
        ordering = ['-time']


class SkillsPR(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, verbose_name="Сотрудник")
    process = models.ForeignKey(Processes, on_delete=models.DO_NOTHING, to_field="process", verbose_name="Процесс")
    level = models.ForeignKey(Levels, on_delete=models.DO_NOTHING, to_field="level", verbose_name="Уровень")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время оценки")

    def __str__(self):
        return f"{self.employee} - {self.process} ({self.level})"

    class Meta:
        verbose_name = "Навык по процессам"
        verbose_name_plural = "Навыки по процессам"
        ordering = ['-time']