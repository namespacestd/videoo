from django.db import models
from django.db.models import Avg
from movie import tmdb
from django import forms
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import date
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
        Get movie details. Will retrieve from the db if it has been previously
        queried, otherwise will get from the TMDB web service.
        """
        # Check if movie already exists in the database
        matching_movies = Movie.objects.filter(m_id=movie_id)
        if len(matching_movies) > 0:
            movie = matching_movies[0]
            logger.info('Found movie %s in db.', movie_id)
        else:
            # If movie does not exist in the database, retrieve details from TMDB
            tmdb_item = tmdb.get_details_from_tmdb(movie_id)
            movie = Movie.convert_to_movie(tmdb_item)
            movie.save()
            # get it from the DB again, since the format of dates is different
            # in the API JSON compared to the DB
            movie = Movie.objects.get(m_id=movie_id)
            logger.info('Retrieved movie #%s from tmdb.', movie_id)

        # Populate calculated fields
        avg = models.Avg('rating')
        ratings = Rating.objects.exclude(rating=-1).filter(movie=movie)
        movie.avg_rating = ratings.aggregate(avg)['rating__avg']

        return movie

    @staticmethod
    def search(search_term, page=1):
        """
        Search for movies matching the search_term.  Will only retrieve
        a subset of the fields--enough to show in the results list.
        """
        search_results = tmdb.search_for_movie_by_title(search_term, page)
        matched_movies = search_results['results']
        num_items = search_results['total_results']
        num_pages = search_results['total_pages']
        response_page = search_results['page']
        if response_page != page:
            logger.error("Response page does not match requested page: %s != %s",
                         response_page, page)
        logger.info('Found list of movies in db: ' + str(matched_movies))
        return {
            'items': [Movie.convert_to_movie(a) for a in matched_movies if a is not None],
            'total_items': num_items,
            'total_pages': num_pages,
            'page': page,
            'search_term': search_term,
        }

    @staticmethod
    def get_popular(min_rating=3):
        """
        Gets the list of most popular movies from Videe-o. Gets all
        movies in descending order of their average rating.
        Excludes any movies with a rating lower than 'min_rating'.
        """
        # gets back a list of movie ids, in descending order of rating
        movie_results = Rating.objects.values('movie__m_id').annotate(rating=Avg('rating'))\
            .order_by('-rating').filter(rating__gte=min_rating)
        movie_ids = [m['movie__m_id'] for m in movie_results]
        # trickery to make sure they stay in the right order, but get back the entire movie objects.
        # http://stackoverflow.com/questions/4916851/django-get-a-queryset-from-array-of-ids-in-specific-order
        movies = Movie.objects.filter(m_id__in=movie_ids)
        movies_dict = dict([(obj.m_id, obj) for obj in movies])
        sorted_movies = [movies_dict[m_id] for m_id in movie_ids]
        logger.info(sorted_movies)
        logger.info('Found %s popular items based on Videe-o ratings.' % len(sorted_movies))
        return {
            'items': sorted_movies,
            'total_items': len(sorted_movies),
            'total_pages': 1,
            'current_page': 1
        }

    @staticmethod
    def get_similar(movie_id, page=1):
        matching_movies = tmdb.get_similar(movie_id, page)
        logger.info('Found list of movies in db: ' + str(matching_movies))
        return {
            'items': [Movie.convert_to_movie(a)
                      for a in matching_movies['results'] if a is not None],
            'total_items': matching_movies['total_results'],
            'total_pages': matching_movies['total_pages'],
            'page': matching_movies['page'],
            'current_page': page
        }

    @staticmethod
    def get_genres():
        return tmdb.get_genre_list()

    @staticmethod
    def get_movies_for_genre(genre_id, page=1):
        matching_movies = tmdb.get_movies_for_genre(genre_id, page)
        logger.info('Found list of movies in db: ' + str(matching_movies))
        return {
            'items': [Movie.convert_to_movie(a)
                      for a in matching_movies['results'] if a is not None],
            'total_items': matching_movies['total_results'],
            'total_pages': matching_movies['total_pages'],
            'page': matching_movies['page'],
            'current_page': page
        }

    @staticmethod
    def convert_to_movie(api_movie_obj):
        """
        Generic method to parse movie objects from tmdb_api return
        objects. Works for getting single item detail as parsing
        movies that come back in a list
        """
        # Sometimes the api passes back null movies.  Weird, I know. - Matt M
        if api_movie_obj is None:
            logger.warn('Blank movie encountered')
            return Movie()
        logger.info('Converting to movie: %s (%s)' % (api_movie_obj['title'], api_movie_obj['id']))
        movie = Movie()
        movie.m_id = api_movie_obj['id']
        movie.title = api_movie_obj['title']
        if 'poster_path' in api_movie_obj.keys() and api_movie_obj['poster_path']:
            # w185 indicates api request for the 185px-width image
            movie.poster_path = '%sw185%s' % (tmdb.get_base_url(), api_movie_obj['poster_path'])
        else:
            movie.poster_path = '/static/img/placeholder-poster.jpg'
        movie_keys = api_movie_obj.keys()
        movie.release_date = api_movie_obj['release_date'] if ('id' in movie_keys) else None
        movie.overview = api_movie_obj['overview'] if ('overview' in movie_keys) else None
        movie.budget = api_movie_obj['budget'] if ('budget' in movie_keys) else None
        movie.revenue = api_movie_obj['revenue'] if ('revenue' in movie_keys) else None
        logger.info('Conversion successful')
        return movie

    def __str__(self):
        return "".join([str(self.title), " (", str(self.m_id), ")"])


class Profile(models.Model):
    """
    User profile, with a link to the user object
    """
    user = models.ForeignKey(User)
    email_address = models.CharField(max_length=100)
    join_date = models.DateField()
    user_banned = models.BooleanField(default=False)

    def set_to_superuser(self, current_user):
        if not current_user.is_superuser:
            raise Exception('Access denied. Only superusers may perform this function.')
        if not self.user.is_superuser:
            self.user.is_superuser = True
            self.user.save()

    def set_to_banned(self, current_user):
        if not current_user.is_superuser:
            raise Exception('Access denied. Only superusers may perform this function.') 
        if not self.user.is_superuser:
            self.user_banned = True
            self.user.is_active = False
            self.user.save()
            self.save()
            # Needs comment! What is this line doing?
            [s.delete() for s in Session.objects.all()
             if s.get_decoded().get('_auth_user_id') == self.user.id]

    def remove_ban(self, current_user):
        if not current_user.is_superuser:
            raise Exception('Access denied. Only superusers may perform this function.') 
        if not self.user.is_superuser:
            self.user_banned = False
            self.user.is_active = True
            self.user.save()
            self.save()

    @staticmethod
    def get(user):
        # If parameter is empty, return nothing
        if user is None or not user.username:
            return None

        # Check if profile exists, and return it if it does
        results = Profile.objects.filter(user=user)
        try:
            return results[0]
        except IndexError:
            return None

    @staticmethod
    def search(search_term):
        return Profile.objects.filter(user__username__contains=search_term)

    @staticmethod
    def find(username):
        matches = Profile.objects.filter(user__username__iexact=username)
        if len(matches):
            return matches[0]
        else:
            return None

    @staticmethod
    def create_new_user(username, email_address, password, join_date):
        user = User.objects.create_user(username, email_address, password)
        profile = Profile()
        profile.user = user
        profile.email_address = email_address
        profile.join_date = join_date
        profile.save()
        return profile

    def __str__(self):
        return "".join([str(self.user.username), " (", str(self.user.id), ")"])


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

    def __str__(self):
        return "".join([str(self.rating), " {", str(self.user), ", ", str(self.movie), "}"])


class UserList(models.Model):
    user = models.ForeignKey(Profile, null=False)
    list_name = models.CharField(max_length=30)
    can_delete = models.BooleanField(null=False, default=True)

    @staticmethod
    def create_default_lists(user):
        logger.info("Creating default user lists for user %s", user)
        watched = UserList(user=user, list_name='Watched', can_delete=False)
        watched.save()
        planning = UserList(user=user, list_name='Planning to Watch', can_delete=False)
        planning.save()

    def __str__(self):
        return "".join([str(self.user), ":", str(self.list_name)])


class UserListItem(models.Model):
    user_list = models.ForeignKey(UserList, null=False)
    movie = models.ForeignKey(Movie, null=False)
    rating = models.ForeignKey(Rating, null=False)

    def __str__(self):
        return "".join([str(self.movie), " {", str(self.user_list), "}"])


class Review(models.Model):
    user = models.ForeignKey(Profile)
    movie = models.ForeignKey(Movie)
    date_created = models.DateTimeField()
    date_edited = models.DateTimeField(blank=True, null=True)
    review_body = models.CharField(max_length=REVIEW_MAX_LENGTH)
    # review_tagline?
    review_title = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    # Supersedes default delete method. This method enforces the rule
    # that only the review author or an admin can delete a review.
    def delete(self, current_user):
        if current_user is None:
            raise Exception('Unknown user. Only administrators may delete a review.')
        profile = Profile.get(current_user)

        # If admin, allow delete
        if profile is not None and profile.user.is_superuser:
            super(Review, self).delete()

        # If the author of the review, allow delete
        elif profile is not None and self.user == profile:
            super(Review, self).delete()

        # Otherwise, the user is not allowed to delete the review
        else:
            raise Exception('Only administrators may delete a review')

    def __str__(self):
        return "".join([str(self.review_title), " {", str(self.user), ", ", str(self.movie), "}"])


class ReviewRating(models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(Profile)
    vote = models.IntegerField(default=0)    

    def __str__(self):
        return "".join([str(self.vote), " {", str(self.user), ", ", str(self.review), "}"])


class CreateAccountForm(forms.Form):
    """
    Account creation form, including username, password and email address.
    """
    username = forms.RegexField(
        label="Username",
        max_length=30,
        regex=r'^[\w-]{6,30}$',
        help_text="Required. Between 6 and 30 characters. Letters, digits and -/_ only.",
        error_messages={'invalid': "This value may contain only letters, \
                                    numbers and -/_ characters, and must \
                                    be between 6 and 30 characters long."})
    password1 = forms.CharField(
        label="Password",
        min_length=6,
        max_length=30,
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        min_length=6,
        max_length=30,
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")
    email_address = forms.CharField(label="Email address")  # TODO: change to regexfield

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            if Profile.find(username=username):
                logger.info("Found duplicate username in database.")
            else:
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
        return Profile.create_new_user(username, email_address, password, date.today())
