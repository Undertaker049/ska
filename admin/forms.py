from django import forms
from self_assessment.models import Employees, Department


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['name', 'department', 'subordinate_of', 'is_supervisor', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'subordinate_of': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }