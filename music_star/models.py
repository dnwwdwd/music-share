from django.db import models

class MusicStar(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    musicId = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id