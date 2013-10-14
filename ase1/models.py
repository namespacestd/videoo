from django.db import models
from movie.tmdb import *
from django import forms
from django.contrib.auth.models import User

import urlparse
import logging

logger = logging.getLogger('root.' + __name__)

REVIEW_MAX_LENGTH = 1000

class Movie(models.Model):
    m_id = models.IntegerField()
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)
    release_date = models.DateField()
    # Maybe
    overview = models.CharField(max_length=300)
    budget = models.IntegerField()
    revenue = models.IntegerField()

    # fields that are calculated and populated by get_details method
    avg_rating = 'n/a'

    @staticmethod
    def get_details(movie_id):
        """
        Get movie details. Will retrieve from the db if it has been previously queried, otherwise will get from
        the TMDB web service.
        """
        # Check if movie already exists in the database
        matching_movies = Movie.objects.filter(m_id=movie_id)
        if len(matching_movies) > 0:
            movie = matching_movies[0]
            logger.info('Found movie %s in db.', movie_id)
        else:
            try:
                # If movie does not exist in the database, retrieve details from TMDB
                tmdb_item = Tmdb.get_details_from_tmdb(movie_id)
                movie = Movie()
                movie.m_id = tmdb_item['id']
                movie.title = tmdb_item['title']
                movie.poster_path = Tmdb.get_base_url() + 'w185' + tmdb_item['poster_path']
                movie.release_date = tmdb_item['release_date']
                movie.overview = tmdb_item['overview']
                movie.budget = tmdb_item['budget']
                movie.revenue = tmdb_item['revenue']
                movie.save()
                logger.info('Retrieved movie #%s from tmdb.', movie_id)
            except URLError:
                logger.exception('Unable to reach tmbd')
                #raise Exception('Unable to reach tmdb.')

        # Populate calculated fields
        movie.avg_rating = Rating.objects.filter(movie=movie).aggregate(models.Avg('rating'))

        return movie

class Profile(models.Model):
    """
    User profile, with a link to the user object
    """
    user = models.ForeignKey(User)
    email_address = models.CharField(max_length=100)

    @staticmethod
    def find(search_term):
        return Profile.objects.filter(user__username__contains=search_term)

    @staticmethod
    def create_new_user(username, email_address, password):
        user = User.objects.create_user(username, email_address, password)
        profile = Profile()
        profile.user = user
        profile.email_address = email_address
        profile.save()
        return profile

class Rating(models.Model):
    user = models.ForeignKey(Profile, null=False)
    movie = models.ForeignKey(Movie, null=False)
    rating = models.IntegerField()

class Review(models.Model):
  user = models.ForeignKey(Profile)
  movie = models.ForeignKey(Movie)
  date_created = models.DateField()
  review_body = models.CharField(max_length=REVIEW_MAX_LENGTH)
  # review_tagline?
  review_title = models.CharField(max_length=100)



class CreateAccountForm(forms.Form):
    """
    Account creation form, including username, password and email address.
    """
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.@+-]{6,30}$',
        help_text="Required. Between 6 and 30 characters. Letters, digits and @/./+/-/_ only.",
        error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters, and must " +
                                   "be between 6 and 30 characters long."})
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")
    email_address = forms.CharField(label="Email address")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self):
        password = self.cleaned_data.get("password1")
        email_address = self.cleaned_data.get("email_address")
        username = self.cleaned_data.get('username')
        return Profile.create_new_user(username, email_address, password)