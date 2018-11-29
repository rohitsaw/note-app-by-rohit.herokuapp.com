from django.db import models
import datetime
# Create your models here.

class Notes(models.Model):
    user = models.CharField(max_length=64)
    heading = models.CharField(max_length=100)
    notes = models.TextField()
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.user}-{self.heading}"