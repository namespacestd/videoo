# The following tests can be run using the command in the root of this project:
#    python manage.py test ase1

from django.test import TestCase
from ase1.models import Profile, Review, Movie, User, Rating, CreateAccountForm
from movie import tmdb
from datetime import date
from mock import patch
from selenium import webdriver


class ProfileTests(TestCase):
    """
    Tests methods relating to user profiles on the Videe-o site.
    """

    def test_search_users(self):
        Profile.create_new_user('uniquetestuser', 'none@none.com', 'password1', date.today())
        found = Profile.search('uniquetest')
        #for profile in found:
        #    user = profile.user
        self.assertTrue(len(found) > 0)

    # TESTING EQUIVALENCE PARTITIONS

    # Equivalence Partition: Creating user with less than 6 characters in username is not allowed.
    # Boundary test case: User has 0 characters in username
    def test_create_user_0_char_name(self):
        form = CreateAccountForm(data={
            'username': '',
            'email_address': 'none@none.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertFalse(form.is_valid())

    # Boundary test case: User has 5 characters in username
    def test_create_user_5_char_name(self):
        form = CreateAccountForm(data={
            'username': 'a' * 5,
            'email_address': 'none@none.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertFalse(form.is_valid())

    # Equivalence Partition: Creating with 6-30 characters in username is allowed.
    # Boundary test case: User has 6 characaters in username
    def test_create_user_6_char_name(self):
        form = CreateAccountForm(data={
            'username': 'a' * 6,
            'email_address': 'none@none.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertTrue(form.is_valid())
        form.save()

    # Boundary test case: User has 6 characaters in username
    def test_create_user_30_char_name(self):
        form = CreateAccountForm(data={
            'username': 'a' * 30,
            'email_address': 'none@none.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertTrue(form.is_valid())
        form.save()

    # Equivalence Partition: Creating user with more than 30 characters in username is not allowed.
    # Boundary test case: User has 31 characters in username
    def test_create_user_31_char_name(self):
        form = CreateAccountForm(data={
            'username': 'a' * 31,
            'email_address': 'none@none.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertFalse(form.is_valid())

    # Boundary test case: User has 9999999 characters in username
    def test_create_user_9999999_char_name(self):
        form = CreateAccountForm(data={
            'username': 'a' * 9999999,
            'email_address': 'none@none.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertFalse(form.is_valid())

    # Equivalence Partition: Creating user with less than 6 characters in password is not allowed.
    # Boundary test case: User has 0 characters in password
    def test_create_user_0_char_password(self):
        form = CreateAccountForm(data={
            'username': 'testuser',
            'email_address': 'none@none.com',
            'password1': '',
            'password2': ''
        })
        self.assertFalse(form.is_valid())

    # Boundary test case: User has 5 characters in password
    def test_create_user_5_char_password(self):
        form = CreateAccountForm(data={
            'username': 'testuser',
            'username': 'a' * 5,
            'email_address': 'none@none.com',
            'password1': 'a' * 5,
            'password2': 'a' * 5
        })
        self.assertFalse(form.is_valid())

    # Equivalence Partition: Creating with 6-30 characters in password is allowed.
    # Boundary test case: User has 6 characaters in password
    def test_create_user_6_char_password(self):
        form = CreateAccountForm(data={
            'username': 'testuser',
            'email_address': 'none@none.com',
            'password1': 'a' * 6,
            'password2': 'a' * 6
        })
        self.assertTrue(form.is_valid())
        form.save()

    # Boundary test case: User has 6 characaters in password
    def test_create_user_30_char_password(self):
        form = CreateAccountForm(data={
            'username': 'testuser',
            'email_address': 'none@none.com',
            'password1': 'a' * 30,
            'password2': 'a' * 30
        })
        self.assertTrue(form.is_valid())
        form.save()

    # Equivalence Partition: Creating user with more than 30 characters in password is not allowed.
    # Boundary test case: User has 31 characters in password
    def test_create_user_31_char_password(self):
        form = CreateAccountForm(data={
            'username': 'testuser',
            'email_address': 'none@none.com',
            'password1': 'a' * 31,
            'password2': 'a' * 31
        })
        self.assertFalse(form.is_valid())

    # Boundary test case: User has 9999999 characters in password
    def test_create_user_9999999_char_password(self):
        form = CreateAccountForm(data={
            'username': 'testuser',
            'email_address': 'none@none.com',
            'password1': 'a' * 9999999,
            'password2': 'a' * 9999999
        })
        self.assertFalse(form.is_valid())

    # Equivalence Partition: Searching should allow search terms of 1 or more characters
    # Boundary test case: Search term has 1 character
    def test_search_for_profile_1_chars(self):
        Profile.create_new_user('uniquetestuser', 'none@none.com', 'password1', date.today())
        with self.assertRaises(tmdb.QueryException):
            found = Profile.search('t')

    # Boundary test case: Search term has 9999999 characters (valid, but could never return any results)
    def test_search_for_profile_9999999_chars(self):
        Profile.create_new_user('uniquetestuser', 'none@none.com', 'password1', date.today())
        found = Profile.search('t' * 9999999)
        self.assertTrue(len(found) == 0)

    # Equivalence Partition: Searching should not allow search terms of less than 1 characters
    # Boundary test case: Search term has 0 characters (this tests the upper and lower bound of the partition)
    def test_search_for_profile_0_chars(self):
        Profile.create_new_user('uniquetestuser', 'none@none.com', 'password1', date.today())
        with self.assertRaises(tmdb.QueryException):  # Verify that exception is raised, as it should be
            found = Profile.search('')  # A search with 0 characters should throw an exception

    # Equivalence Partition: Getting a user by username
    # Boundary test case: Attempting to get a user that does not exist should return that user
    def test_find_user_when_exists(self):
        profile = Profile.create_new_user('testuser1', 'none@none.com', 'password1', date.today())
        profile_found = Profile.find('testuser1')
        self.assertTrue(profile_found == profile)

    # Boundary test case: Attempting to get a user that does not exist should return a null value
    def test_find_user_when_does_not_exist(self):
        profile = Profile.create_new_user('testuser1', 'none@none.com', 'password1', date.today())
        profile_found = Profile.find('auserthatdoesntexist')
        self.assertTrue(profile_found is None)


class TmdbTests(TestCase):
    """
    Tests the methods that retrieve data from the API.
    """

    # BASIC FUNCTIONALITY TESTS
    def test_get_api_key(self):
        """
        Tests that the API key can be read
        """
        api_key = tmdb.get_api_key()
        self.assertTrue(api_key, 'Key was returned empty.')

    def test_get_movie_list(self):
        results = tmdb.search_for_movie_by_title('Fire', 1)
        self.assertTrue(len(results), 'Search for "Fire" returned 0 results. Expected more.')

    def test_get_popular_list(self):
        results = tmdb.get_popular_movies(1)
        self.assertTrue(len(results), 'Search for "Fire" returned 0 results. Expected more.')

    def test_get_single_movie(self):
        movie = tmdb.get_details_from_tmdb(513)
        self.assertTrue(movie['original_title'] == 'Fire')

    def test_get_movie_details(self):
        ret = tmdb.get_details_from_tmdb(513)
        with patch.object(tmdb, "get_details_from_tmdb", return_value=ret) as m_method:
            Movie.get_details(513)  # this should get it from TMDB api
            m_method.assert_called_with(513)
            m_method.reset_mock()
            Movie.get_details(513)  # this should get it from the SQL database
            self.assertFalse(m_method.called)

    def test_get_base_url(self):
        base_url = tmdb.get_base_url()
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
        profile = Profile.create_new_user('testing5', 'none@none.com', 'testing5', date.today())
        movie = Movie.get_details(11)
        Rating.set_rating_for_user(movie,4,profile)
        movie = Movie.get_details(12)
        Rating.set_rating_for_user(movie,5,profile)
        movie = Movie.get_details(13)
        Rating.set_rating_for_user(movie,2,profile)
        results = Movie.get_popular(min_rating=3)
        self.assertTrue(results['total_items'] == 2)

    # TESTING EQUIVALENCE PARTITIONS

    # Equivalence Partition: Searching for movie titles that do exist with search terms of valid lengths
    # Boundary test case: Performing valid search with a one-character search term
    def test_search_for_movies_1_char_search_term(self):
        with self.assertRaises(tmdb.QueryException):
            total_items = Movie.search(search_term='')['total_items']

    # Boundary test case: Performing valid search with a long, obscure, but valid, search term: 'guadalquivir'
    def test_search_for_movies_12_char_search_term(self):
        total_items = Movie.search(search_term='guadalquivir')['total_items']
        self.assertTrue(total_items > 0)

    # Equivalence Partition: Searching for movie titles that do exist with varying numbers of terms in the search phrase
    # Boundary test case: Performing valid search with a one-word search phrase
    def test_search_for_movies_1_word_search_phrase(self):
        total_items = Movie.search(search_term='juno')['total_items']
        self.assertTrue(total_items > 0)

    # Boundary test case: Performing valid search with a long, -word search phrase
    def test_search_for_movies_8_word_search_phrase(self):
        total_items = Movie.search(search_term='The Legend of Hell''s Gate An American Conspiracy')['total_items']
        self.assertTrue(total_items > 0)

    # Equivalence Partition: Getting most popular movies (for testing purposes, one movie exists for each rating level)
    # Boundary test case: Getting poular movies when the definition of 'popular' is 1 stars or higher
    def test_get_popular_movies_min_1_star(self):
        profile = Profile.create_new_user('testing1', 'none@none.com', 'testing1', date.today())
        movie = Movie.get_details(11)
        Rating.set_rating_for_user(movie, 1, profile)
        movie = Movie.get_details(12)
        Rating.set_rating_for_user(movie, 2, profile)
        movie = Movie.get_details(13)
        Rating.set_rating_for_user(movie, 3, profile)
        movie = Movie.get_details(513)
        Rating.set_rating_for_user(movie, 4, profile)
        movie = Movie.get_details(5)
        Rating.set_rating_for_user(movie, 5, profile)
        # All 5 movies should show up as results when the minimum rating required for a movie to be 'popular' is a 1
        self.assertTrue(Movie.get_popular(min_rating=1)['total_items'] == 5)

    # Boundary test case: Getting poular movies when the definition of 'popular' is 5 stars or higher
    def test_get_popular_movies_min_5_stars(self):
        profile = Profile.create_new_user('testing1', 'none@none.com', 'testing1', date.today())
        movie = Movie.get_details(11)
        Rating.set_rating_for_user(movie, 1, profile)
        movie = Movie.get_details(12)
        Rating.set_rating_for_user(movie, 2, profile)
        movie = Movie.get_details(13)
        Rating.set_rating_for_user(movie, 3, profile)
        movie = Movie.get_details(513)
        Rating.set_rating_for_user(movie, 4, profile)
        movie = Movie.get_details(5)
        Rating.set_rating_for_user(movie, 5, profile)
        # There should only be one result when getting movies with rating 5 or higher
        self.assertTrue(Movie.get_popular(min_rating=5)['total_items'] == 1)


class ReviewsTests(TestCase):
    """
    Tests user reviews of movies.

    Note: These tests were built as a part of writing the original methods, not 
    as a part of the testing assignment.
    """

    def test_delete_review_user_is_admin(self):
        profile = Profile.create_new_user('test11', 'test@none.com', 'test11', date.today())
        profile.user.is_superuser = True
        profile.user.save()
        profile.save()
        movie = Movie.get_details(5)
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
        movie = Movie.get_details(5)
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
        movie = Movie.get_details(5)
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
        movie = Movie.get_details(5)
        new_review = Review()
        new_review.review_title = 'Test review'
        new_review.review_body = 'body'
        new_review.date_created = '2012-12-12'
        new_review.user = profile
        new_review.movie = movie
        new_review.save()
        with self.assertRaises(Exception):  # Verify that error is raised when trying to do this since user is not admin
            new_review.delete()


class BrowserTests(TestCase):
    """
    Tests urls and views code.
    """
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()

    def test_spotlight(self):
        self.browser.get("http://127.0.0.1:8000/")
        self.browser.find_element_by_id("movie-spotlight").find_element_by_tag_name("img").click()
        self.assertEqual(self.browser.current_url, "http://127.0.0.1:8000/movie/detail/5/")

    # Metamorphic Property: if the user is not logged in, he should not be able to rate movies
    def test_rating_absence(self):
        self.browser.get("http://127.0.0.1:8000/movie/detail/5/")
        self.assertFalse(self.browser.find_elements_by_id("rating-stars"))

    def test_profile(self):
        self.browser.get("http://127.0.0.1:8000/profile")
        self.assertFalse(self.browser.find_elements_by_id("rating-stars"))

    def test_