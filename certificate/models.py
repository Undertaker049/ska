from django.db import models

TYPES = {"CER": "certification", "TR": "training", "EX": "exam"}


class CertificateCategory(models.Model):
    category = models.CharField(max_length=128, unique=True)


class CertificateSubCategory(models.Model):
    subcategory_of = models.ForeignKey(CertificateCategory, on_delete=models.CASCADE, to_field="category")
    subcategory = models.CharField(max_length=128, unique=True)


class Certificate(models.Model):
    employee_name = models.CharField(max_length=128)
    training_name = models.CharField(max_length=256)
    training_type = models.CharField(max_length=13, choices=TYPES)
    date = models.DateField()
    category = models.ForeignKey(CertificateCategory, on_delete=models.DO_NOTHING, to_field="category")
    sub_category = models.ForeignKey(CertificateSubCategory, null=True,  on_delete=models.DO_NOTHING, to_field="subcategory")
    certificate_file = models.FileField(upload_to="certificates")
