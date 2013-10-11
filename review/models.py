from django.db import models
from profile.models import *
from movie.models import *

REVIEW_MAX = 1000

class Review(models.Model):
  user = models.ForeignKey(Profile)
  movie = models.ForeignKey(Movie)
  date_created = models.DateField()
  review_body = models.CharField(max_length=REVIEW_MAX)
  # review_tagline?
  review_title = models.CharField(max_length=100)

