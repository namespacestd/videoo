from django.db import models

class Movie(models.Model):
  title = models.CharField(max_length=100)
  m_id = models.IntegerField()
  poster_path = models.CharField(max_length=100)
  release_date = models.DateField()
  # Maybe
  overview = models.CharField(max_length=300)
  budget = models.IntegerField()
  revenue = models.IntegerField()
