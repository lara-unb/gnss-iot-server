from django.db import models
from django.contrib.auth.models import User
from django.core.management.utils import get_random_secret_key
# Create your models here.


class Receiver(models.Model):
    name = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DataGnss(models.Model):
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
    info_receiver = models.TextField()
    info_server = models.TextField()
    info_satellite = models.TextField()
    status_algorithm = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
