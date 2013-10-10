from django.db import models

class Rating:
  user = models.ForeignKey(Profile)
  movie = models.ForeignKey(Movie)
  rating = models.IntegerField()
