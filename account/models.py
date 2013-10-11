from django.db import models

class Profile(models.Model):
  username = models.CharField(max_length=100)
