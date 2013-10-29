# The following tests can be run using the command in the root of this project:
#    python manage.py test ase1

from django.test import TestCase
from ase1.models import Profile, Review, Movie, User, Tmdb, Rating

class ReviewsTests(TestCase):

    def test_delete_review_user_is_admin(self):
        profile = Profile.create_new_user('mrrmmm', 'mrrm@none.com', 'mrrmmmmmmm11')
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

    def test_delete_review_user_is_not_admin(self):
        print 'Testing test_delete_review_user_is_not_admin'
        profile = Profile.create_new_user('mrrmmm', 'mrrm@none.com', 'mrrmmmmmmm11')
        movie = Movie.get_details(5);
        new_review = Review()
        new_review.review_title = 'Test review'
        new_review.review_body = 'body'
        new_review.date_created = '2012-12-12'
        new_review.user = profile
        new_review.movie = movie
        new_review.save(profile.user)
        with self.assertRaises(Exception):  # Verify that error is raised when trying to do this since user is not admin
            new_review.delete()

class ProfileTests(TestCase):

    def test_create_user(self):
        Profile.create_new_user('mrrm', 'mrrm@none.com', 'mrrm')
        print 'List of all users:'
        for user in User.objects.all():
            print '  Username: %s   Email: %s' % (user.username, user.email)

    def test_search_users(self):
        Profile.create_new_user('mrm1', 'mrm@none.com', 'mrm1')
        found = Profile.find('Mrm')
        for profile in found:
            user = profile.user
            print '  Username: %s   Email: %s' % (user.username, user.email)
        self.assertTrue(len(found) > 0)

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

    def test_get_popular_movies(self):
        movies = Movie.get_popular()
        self.assertTrue(movies)

    def test_get_popular_movies_pages(self):
        page1 = Movie.get_popular(1)
        page2 = Movie.get_popular(2)
        print page1['items'][0].title
        print page2['items'][0].title
        self.assertTrue(page1['items'][0].title!=page2['items'][0].title)

    def test_get_similar_movies(self):
        movies = Movie.get_similar(11)
        print movies
        self.assertTrue(movies)

    def test_get_generes(self):
        genres = Movie.get_genres()
        print genres
        self.assertTrue(genres)

    def test_get_movies_for_genre(self):
        genres = Movie.get_genres()
        movies = Movie.get_movies_for_genre(genres[0][0], 1)
        print movies
        self.assertTrue(movies)

    def test_get_overall_most_popular(self):
        print 'Overall most popular:'
        profile = Profile.create_new_user('testing5', 'mrrm@none.com', 'testing5')
        movie = Movie.get_details(11)
        Rating.set_rating_for_user(movie,4,profile)
        movie = Movie.get_details(12)
        Rating.set_rating_for_user(movie,5,profile)
        movie = Movie.get_details(13)
        Rating.set_rating_for_user(movie,2,profile)
        results = Movie.get_overall_most_popular_movies()
        print results
        self.assertTrue(len(results) == 2)