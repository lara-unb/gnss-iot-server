from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=20)
    # coord_x =models.IntegerField()
    # coord_y =models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()

    def __str__(self):
        return self.name
    