from django.db import models


class Reviews(models.Model):
    message = models.TextField()
    reviewer_id = models.IntegerField()
    reviewed_id = models.IntegerField()
    block = models.CharField(max_length=2)
    theme = models.TextField()
