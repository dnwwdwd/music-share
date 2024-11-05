from django.db import models

class Singer(models.Model):
    id = models.AutoField(primary_key=True)
    imgUrl = models.URLField(max_length=500)
    name = models.CharField(max_length=50)
    songCount = models.IntegerField(default=0)
    description = models.CharField(max_length=500)
    def __str__(self):
        return self.name