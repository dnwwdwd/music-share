from django.db import models

class Music(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    imgUrl = models.CharField(max_length=256)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    duration = models.CharField(max_length=10)
    singerId = models.IntegerField()
    userId = models.IntegerField()
    heat = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name