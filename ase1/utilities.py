from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core import management
from datetime import date
from .models import Profile, Review, Movie, User, Rating

import logging

logger = logging.getLogger('root.' + __name__)

class AppInitialization():

    @staticmethod
    def initialize_database():
        # Initialization code.  This will be run once and only once after all 
        # the models above are loaded.  It makes sure all testing data is loaded in.
        logger.info('Initializing database...')

        # Creates the database if none exists
        management.call_command('syncdb', interactive=False)

        # Load testing data
        if settings.AUTOLOAD_TESTING_DATA:
            if not User.objects.count():
                logger.info('Loading initial data since AUTOLOAD_TESTING_DATA is set to true...')
                AppInitialization.populate_testing_data()

        # Ensure super user exists.
        if settings.AUTOLOAD_ADMIN_ACCOUNT:
            su = User.objects.filter(username='ase1')
            if not su:
                # Ensure that default super-user exists. This check is placed here because
                # it affects performance the least here, and it's the first time the superuser
                # credentials could matter.
                logger.info('Creating initial superuser since AUTOLOAD_ADMIN_ACCOUNT is set to true...')
                su = Profile.create_new_user('ase1', '', 'password123', date.today())
                su.user.is_superuser = True
                su.user.save()


    @staticmethod
    def populate_testing_data():
        """
        This method is used to populate testing data for black-box, grey-box, and 
        white-box testing.  It can be used in the setup for unit tests, or run on
        a development database to populate some initial data.  It will be especially
        useful when a schema changes, and the entire database needs to be recreated.
        """

        # Create users
        user1 = Profile.create_new_user('testuser1', 'testuser1@none.com', 'test', date.today())
        user2 = Profile.create_new_user('testuser2', 'testuser2@none.com', 'test', date.today())
        user3 = Profile.create_new_user('testuser3', 'testuser3@none.com', 'test', date.today())
        user4 = Profile.create_new_user('testuser4', 'testuser4@none.com', 'test', date.today())

        # Get movies
        avalanche = Movie.get_details(166680)
        life_without_me = Movie.get_details(20)
        magnetic_rose = Movie.get_details(30)
        million_dollar_baby = Movie.get_details(70)
        independence_day = Movie.get_details(602)
        the_matrix = Movie.get_details(603)
        black_hawk_down = Movie.get_details(855)

        # Rate a bunch of movies
        Rating.set_rating_for_user(movie=avalanche,stars=4,profile=user1)
        Rating.set_rating_for_user(movie=avalanche,stars=5,profile=user2)
        Rating.set_rating_for_user(movie=life_without_me,stars=4,profile=user3)
        Rating.set_rating_for_user(movie=magnetic_rose,stars=3,profile=user4)
        Rating.set_rating_for_user(movie=million_dollar_baby,stars=5,profile=user3)
        Rating.set_rating_for_user(movie=independence_day,stars=5,profile=user3)
        Rating.set_rating_for_user(movie=the_matrix,stars=5,profile=user3)
        Rating.set_rating_for_user(movie=black_hawk_down,stars=5,profile=user3)

        # Movie reviews
        Review(user=user1,movie=avalanche,review_title='Test review',review_body='body',date_created='2012-12-12').save()
        Review(user=user2,movie=avalanche,review_title='Test review',review_body='body',date_created='2012-12-12').save()
