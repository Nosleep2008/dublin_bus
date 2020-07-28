from django.db import models


class Favourite(models.Model):
    username = models.CharField(max_length=20, verbose_name="origin_stop", default='')
    origin = models.CharField(max_length=100, verbose_name="origin_stop", default='')
    destination = models.CharField(max_length=100, verbose_name="destination_stop", default='')

    # def __str__(self):
    #     return self.username, self.origin, self.destination