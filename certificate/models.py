from django.db import models

from self_assessment.models import Employees

TYPES = [("CER", "certification"), ("TR", "training"), ("EX", "exam")]

class CertificateCategory(models.Model):
    category = models.CharField(max_length=128, unique=True)


class CertificateSubCategory(models.Model):
    subcategory_of = models.ForeignKey(CertificateCategory, on_delete=models.CASCADE, to_field="category")
    subcategory = models.CharField(max_length=128, unique=True)


class Certificate(models.Model):
    employee = models.ForeignKey(Employees, null=True, on_delete=models.CASCADE, to_field="id")
    training_name = models.CharField(max_length=256)
    training_type = models.CharField(max_length=13, choices=TYPES)
    date = models.DateField()
    category = models.ForeignKey(CertificateCategory, on_delete=models.DO_NOTHING, to_field="category")
    sub_category = models.ForeignKey(CertificateSubCategory, null=True,  on_delete=models.DO_NOTHING, to_field="subcategory")
    certificate_file = models.FileField(upload_to="certificates")
