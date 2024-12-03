from django import forms
from self_assessment.models import Employees, Department

# Форма для создания и редактирования сотрудников
class EmployeeForm(forms.ModelForm):

    # Валидация полей в зависимости от роли сотрудника
    class Meta:
        model = Employees
        fields = ['name', 'department', 'subordinate_of', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'subordinate_of': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }

    # Валидация данных формы
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        subordinate_of = cleaned_data.get('subordinate_of')

        if role == 'employee' and not subordinate_of:
            raise forms.ValidationError({'subordinate_of': 'Сотрудник должен иметь руководителя'})

        if role in ['supervisor', 'admin']:
            cleaned_data['subordinate_of'] = None

        if role == 'admin':
            cleaned_data['department'] = None

        return cleaned_data

    # Динамическое определение списка полей формы в зависимости от роли
    def get_fields(self):
        fields = ['name', 'role']

        if self.instance.role != 'admin':
            fields.extend(['department', 'subordinate_of'])

        return fields

# Форма для создания и редактирования отделов
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }