from django.db import models
from movie.tmdb import *
from django import forms
from django.contrib.auth.models import User

import logging

logger = logging.getLogger('root.' + __name__)

REVIEW_MAX_LENGTH = 1000


class Movie(models.Model):
    m_id = models.IntegerField()
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100, null=True)
    release_date = models.DateField(null=True)
    overview = models.CharField(max_length=300, null=True)
    budget = models.IntegerField(null=True)
    revenue = models.IntegerField(null=True)

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
            # If movie does not exist in the database, retrieve details from TMDB
            tmdb_item = Tmdb.get_details_from_tmdb(movie_id)
            movie = Movie.convert_to_movie(tmdb_item)
            movie.save()
            # get it from the DB again, since the format of dates is different in the API JSON compared to the DB
            movie = Movie.objects.get(m_id=movie_id)
            logger.info('Retrieved movie #%s from tmdb.', movie_id)

        # Populate calculated fields
        movie.avg_rating = Rating.objects.exclude(rating=-1).filter(movie=movie).aggregate(models.Avg('rating'))['rating__avg']

        return movie

    @staticmethod
    def search(search_term, page=1):
        """
        Search for movies matching the search_term.  Will only retrieve a subset of the fields--enough to show in the
        results list.
        """
        matching_movies = Tmdb.search_for_movie_by_title(search_term)
        logger.info('Found list of movies in db: ' + str(matching_movies))
        return {
            'items': [Movie.convert_to_movie(a) for a in matching_movies['results'] if a is not None],
            'total_items': matching_movies['total_results'],
            'total_pages': matching_movies['total_pages'],
            'page': matching_movies['page'],
            'search_term': search_term,
            'current_page': page
        }

    @staticmethod
    def get_popular(page=1):
        """
        Search for movies matching the search_term.  Will only retrieve a subset of the fields--enough to show in the
        results list.
        """
        matching_movies = Tmdb.get_popular_movies(page)
        logger.info('Found list of movies in db: ' + str(matching_movies))
        return {
            'items': [Movie.convert_to_movie(a) for a in matching_movies['results'] if a is not None],
            'total_items': matching_movies['total_results'],
            'total_pages': matching_movies['total_pages'],
            'page': matching_movies['page'],
            'current_page': page
        }

    @staticmethod
    def convert_to_movie(api_movie_obj):
        """
        Generic method to parse movie objects from tmdb_api return objects. Works for getting single item detail as
        parsing movies that come back in a list
        """
        # Sometimes the api passes back null movies.  Weird, I know. - Matt M
        if (api_movie_obj == None):
            logger.warn('Blank movie encountered')
            return Movie()
        logger.info('Converting to movie: %s (%s)' % (api_movie_obj['title'], api_movie_obj['id']))
        movie = Movie()
        movie.m_id = api_movie_obj['id']
        movie.title = api_movie_obj['title']
        if 'poster_path' in api_movie_obj.keys() and api_movie_obj['poster_path']:
            # w185 indicates api request for the 185px-width image
            movie.poster_path = '%sw185%s' % (Tmdb.get_base_url(), api_movie_obj['poster_path'])
        else:
            movie.poster_path = '/static/img/placeholder-poster.jpg'
        movie.release_date = api_movie_obj['release_date'] if ('id' in api_movie_obj.keys()) else None
        movie.overview = api_movie_obj['overview'] if ('overview' in api_movie_obj.keys()) else None
        movie.budget = api_movie_obj['budget'] if ('budget' in api_movie_obj.keys()) else None
        movie.revenue = api_movie_obj['revenue'] if ('revenue' in api_movie_obj.keys()) else None
        logger.info('Conversion successful')
        return movie


class Profile(models.Model):
    """
    User profile, with a link to the user object
    """
    user = models.ForeignKey(User)
    email_address = models.CharField(max_length=100)
    is_admin = models.BooleanField()

    @staticmethod
    def get(user):
        # If parameter is empty, return nothing
        if user is None or not user.username:
            return None

        # Check if profile exists, and return it if it does
        logger.debug(user)
        results = Profile.objects.filter(user=user)
        try:
            return results[0]
        except IndexError:
            return None

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

    @staticmethod
    def get_rating_for_user(profile, movie):
        rating = Rating.objects.filter(user=profile, movie=movie)
        if not len(rating):
            return None
        else:
            return rating[0].rating

    @staticmethod
    def set_rating_for_user(movie, stars, profile):
        rating = Rating.objects.filter(user=profile, movie=movie)
        if not len(rating):
            rating = Rating(movie=movie, user=profile, rating=stars)
            rating.save()
        else:
            rating[0].rating = stars
            rating[0].save()

class MovieList(models.Model):
    MOVIE_STATUS = (
        ('Watching', 'Watching'),
        ('Plan to Watch', 'Plan to Watch'),
        ('Completed', 'Completed'),
    )
    user = models.ForeignKey(Profile, null=False)
    movie = models.ForeignKey(Movie, null=False)
    status = models.CharField(max_length=20, choices=MOVIE_STATUS)
    rating = models.ForeignKey(Rating, null=True)


class Review(models.Model):
    user = models.ForeignKey(Profile)
    movie = models.ForeignKey(Movie)
    date_created = models.DateField()
    review_body = models.CharField(max_length=REVIEW_MAX_LENGTH)
    # review_tagline?
    review_title = models.CharField(max_length=100)

    def delete(self, currentUser):
        if currentUser == None:
            raise Exception('Unknown user. Only administrators may delete a review.')
        profile = Profile.get(currentUser)
        if profile != None and profile.is_admin:
            super(Review, self).delete()
        else:
            raise Exception('Only administrators may delete a review')

class ReviewRating(models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(Profile)
    vote = models.IntegerField(default=0)    


class CreateAccountForm(forms.Form):
    """
    Account creation form, including username, password and email address.
    """
    username = forms.RegexField(
        label="Username",
        max_length=30,
        regex=r'^[\w.@+-]{6,30}$',
        help_text="Required. Between 6 and 30 characters. Letters, digits and @/./+/-/_ only.",
        error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters, and must \
                                   be between 6 and 30 characters long."})
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
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