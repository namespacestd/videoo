# The following tests can be run using the command in the root of this project:
#    python manage.py test ase1

from django.test import TestCase
from ase1.models import Profile, Review, Movie, User, Tmdb, Rating
from datetime import date


class ProfileTests(TestCase):
    '''
    Tests methods relating to user profiles on the Videe-o site.
    '''

    # BASIC FUNCTIONALITY TESTS
    def test_create_user(self):
        Profile.create_new_user('testuser1', 'none@none.com', 'password1', date.today())

    def test_search_users(self):
        Profile.create_new_user('testuser1', 'none@none.com', 'password1', date.today())
        found = Profile.search('testuser1')
        for profile in found:
            user = profile.user
        self.assertTrue(len(found) > 0)

    def test_find_user(self):
        profile = Profile.create_new_user('testuser1', 'none@none.com', 'password1', date.today())
        profile_found = Profile.find('testuser1')
        self.assertTrue(profile == found)

    # TESTING EQUIVALENCE PARTITIONS
    # TODO: Define equivalence partitions, and the boundaries for those, and define tests for them.

    # POLYMORPHIC TESTS DESCRIPTIONS
    # (These are not automated unit tests, but this is a good place to keep their definitions, in comments.)
    # TODO: Write in prose

class TmdbTests(TestCase):
    '''
    Tests the methods that retrieve data from the API.
    '''

    def test_get_api_key(self):
        """
        Tests that the API key can be read
        """
        api_key = Tmdb.get_api_key()
        self.assertTrue(api_key, 'Key was returned empty. Does the api key file exist in your home directory?')

    def test_get_movie_list(self):
        results = Tmdb.search_for_movie_by_title('Fire', 1)
        self.assertTrue(len(results))

    def test_get_single_movie(self):
        movie = Tmdb.get_details_from_tmdb(513)
        self.assertTrue(movie['original_title'] == 'Fire')

    def test_get_movie_details(self):
        Movie.get_details(513) # this should get it from TMDB api
        Movie.get_details(513) # this should get it from the SQL database

    def test_get_base_url(self):
        base_url = Tmdb.get_base_url()
        self.assertTrue(base_url)

    def test_get_similar_movies(self):
        movies = Movie.get_similar(11)
        self.assertTrue(movies)

    def test_get_genres(self):
        genres = Movie.get_genres()
        self.assertTrue(genres)

    def test_get_movies_for_genre(self):
        genres = Movie.get_genres()
        movies = Movie.get_movies_for_genre(genres[0][0], 1)
        self.assertTrue(movies)

    def test_get_overall_most_popular(self):
        print 'Overall most popular:'
        profile = Profile.create_new_user('testing5', 'none@none.com', 'testing5', date.today())
        movie = Movie.get_details(11)
        Rating.set_rating_for_user(movie,4,profile)
        movie = Movie.get_details(12)
        Rating.set_rating_for_user(movie,5,profile)
        movie = Movie.get_details(13)
        Rating.set_rating_for_user(movie,2,profile)
        results = Movie.get_popular(min_rating=3)
        print results
        self.assertTrue(results['total_items'] == 2)


class ReviewsTests(TestCase):
    '''
    Tests user reviews of movies.

    Note: These tests were built as a part of writing the original methods, not 
    as a part of the testing assignment.
    '''

    def test_delete_review_user_is_admin(self):
        profile = Profile.create_new_user('test11', 'test@none.com', 'test11', date.today())
        profile.user.is_superuser = True
        profile.user.save()
        profile.save()
        movie = Movie.get_details(5);
        new_review = Review()
        new_review.review_title = 'Test review'
        new_review.review_body = 'body'
        new_review.date_created = '2012-12-12'
        new_review.user = profile
        new_review.movie = movie
        new_review.save()
        new_review.delete(profile.user)

    def test_delete_review_user_is_writer_of_review(self):
        profile = Profile.create_new_user('test11', 'test@none.com', 'test11', date.today())
        movie = Movie.get_details(5);
        new_review = Review()
        new_review.review_title = 'Test review'
        new_review.review_body = 'body'
        new_review.date_created = '2012-12-12'
        new_review.user = profile
        new_review.movie = movie
        new_review.save()
        new_review.delete(profile.user)

    def test_delete_review_user_is_not_admin(self):
        profile_author = Profile.create_new_user('test11', 'test@none.com', 'test11', date.today())
        profile_nonauthor = Profile.create_new_user('test22', 'test2@none.com', 'test22', date.today())
        movie = Movie.get_details(5);
        new_review = Review()
        new_review.review_title = 'Test review'
        new_review.review_body = 'body'
        new_review.date_created = '2012-12-12'
        new_review.user = profile_author
        new_review.movie = movie
        new_review.save()
        with self.assertRaises(Exception):  # Verify that error is raised when trying to do this since user is not admin
            new_review.delete(profile_nonauthor.user)

    def test_delete_review_no_user_passed_in(self):
        profile = Profile.create_new_user('test11', 'none@none.com', 'test11', date.today())
        movie = Movie.get_details(5);
        new_review = Review()
        new_review.review_title = 'Test review'
        new_review.review_body = 'body'
        new_review.date_created = '2012-12-12'
        new_review.user = profile
        new_review.movie = movie
        new_review.save()
        with self.assertRaises(Exception):  # Verify that error is raised when trying to do this since user is not admin
            new_review.delete()