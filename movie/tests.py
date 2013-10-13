"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from ase1.models import *


class TmdbTests(TestCase):
    def test_get_api_key(self):
        """
        Tests that the API key can be read
        """
        api_key = Tmdb.get_api_key()
        self.assertTrue(api_key, 'Key was returned empty. Does the api key file exist in your home directory?')

    def test_get_movie_list(self):
        Tmdb.search_for_movie_by_title('matt')

    def test_get_single_movie(self):
        movie = Tmdb.get_details_from_tmdb(513)
        self.assertTrue(movie['original_title'] == 'Fire')

    def test_get_movie_details(self):
        Movie.get_details(513) # this should get it from TMDB api
        Movie.get_details(513) # this should get it from the SQL database

    def test_get_base_url(self):
        base_url = Tmdb.get_base_url()
        print 'Base url: %s' % base_url
        self.assertTrue(base_url)