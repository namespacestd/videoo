from django.db import models
from movie.models import *
from profile.models import *

class Rating:
  user = models.ForeignKey(Profile)
  movie = models.ForeignKey(Movie)
  rating = models.IntegerField()
