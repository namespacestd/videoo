from django.db import models
from movie.tmdb import *
import urlparse

class Movie(models.Model):
    m_id = models.IntegerField()
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)
    release_date = models.DateField()
    # Maybe
    overview = models.CharField(max_length=300)
    budget = models.IntegerField()
    revenue = models.IntegerField()

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
            print 'Found movie %s in db.' % movie_id
        else:
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
            print 'Retrieved movie #%s from tmdb.' % movie_id
        return movie
