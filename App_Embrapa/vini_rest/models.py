from django.db import models

# Create your models here.

class plotData(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    url = models.URLField()
    json_data =  models.JSONField()