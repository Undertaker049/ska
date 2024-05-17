from django.db import models

TYPES = {"CER": "certification", "TR": "training", "EX": "exam"}


class Certificate(models.Model):
    name = models.CharField(max_length=128, unique=True)
    training_name = models.CharField(max_length=256)
    type = models.CharField(max_length=13, choices=TYPES)
    date = models.DateField()
    category = models.CharField(max_length=128)
    sub_category = models.CharField(max_length=128, null=True)
    certificate_file = models.FileField()
