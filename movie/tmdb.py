from urllib2 import Request, urlopen, URLError, HTTPError
from os.path import expanduser
import json
import logging
from urllib import urlencode
from collections import OrderedDict

logger = logging.getLogger('root.' + __name__)


class Tmdb:
    api_key = ''
    base_url = ''

    @staticmethod
    def get_api_key():
        """
        Get api key from file in user home directory. This will be put in a static variable, so it should only need
        to be retrieved from the file system once per application run.
        """
        if Tmdb.api_key:
            return Tmdb.api_key
        else:
            # read API key
            path = expanduser('~/.tmdb_api_key')
            try:
                f = open(path, 'r')
                Tmdb.api_key = f.read().replace('\n', '')
            except IOError:
                logger.error('Failed to open API Key file at path %s', path)
                raise

            logger.debug('Using API Key: %s', Tmdb.api_key)
            return Tmdb.api_key

    @staticmethod
    def get_base_url():
        """
        Get base url for Tmdb images.
        """
        if not Tmdb.base_url:
            # get base url from web service
            logger.info('Retrieving base url')
            headers = {'Accept': 'application/json'}
            params = {'api_key': Tmdb.get_api_key()}
            url = 'https://api.themoviedb.org/3/configuration?api_key={api_key}'.format(**params)
            logger.debug('Address used for query: %s', url)

            try:
                # send request to api
                request = Request(url, headers=headers)
                json_response = urlopen(request).read()

                data = json.loads(json_response)
                Tmdb.base_url = data['images']['base_url']
                logger.debug('Base URL: %s', Tmdb.base_url)
            except URLError:
                logger.error('Network Error. API Query Failed.')
                raise

        return Tmdb.base_url

    @staticmethod
    def get_details_from_tmdb(movie_id):
        # prepare request to retrieve matching movies for a search term
        logger.info('Searching for details of movie with id %s', movie_id)
        headers = {'Accept': 'application/json'}
        params = {'api_key': Tmdb.get_api_key(), 'movie_id': movie_id}
        url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'.format(**params)
        logger.debug('Address used for query: %s', url)

        try:
            # send request to api
            request = Request(url, headers=headers)
            json_response = urlopen(request).read()
            logger.debug('Response: %s', json_response)
        except HTTPError:
            logger.error('Invalid API Query.')
            raise
        except URLError:
            logger.error('Network Error. API Query Failed.')
            raise

        data = json.loads(json_response)

        return data

    @staticmethod
    def search_for_movie_by_title(search_term):
        # prepare request to retrieve matching movies for a search term
        logger.info('Searching for movie with title %s', search_term)
        headers = {'Accept': 'application/json'}
        params = urlencode(OrderedDict(api_key=Tmdb.get_api_key(),query=search_term))
        url = 'https://api.themoviedb.org/3/search/movie?%s' % params
        logger.debug('Address used for query: %s', url)

        try:
            # send request to api
            request = Request(url, headers=headers)
            json_response = urlopen(request).read()
            logger.debug('Response: %s', json_response)
        except HTTPError:
            logger.error('Invalid API Query.')
            raise
        except URLError:
            logger.error('Network Error. API Query Failed.')
            raise

        data = json.loads(json_response)
        return data

    @staticmethod
    def get_popular_movies(page):
        # prepare request to retrieve matching movies for a search term
        logger.info('Getting popular movies')
        headers = {'Accept': 'application/json'}
        params = urlencode(OrderedDict(api_key=Tmdb.get_api_key(),page=page))
        url = 'https://api.themoviedb.org/3/movie/popular?%s' % params
        logger.debug('Address used for query: %s', url)

        try:
            # send request to api
            request = Request(url, headers=headers)
            json_response = urlopen(request).read()
            logger.debug('Response: %s', json_response)
        except HTTPError:
            logger.error('Invalid API Query.')
            raise
        except URLError:
            logger.error('Network Error. API Query Failed.')
            raise

        data = json.loads(json_response)
        return data

    @staticmethod
    def get_similar(movie_id, page=1):
        # prepare request to retrieve matching movies for a search term
        logger.info('Getting popular movies')
        headers = {'Accept': 'application/json'}
        params = urlencode(OrderedDict(api_key=Tmdb.get_api_key(), page=page))
        url = 'https://api.themoviedb.org/3/movie/%s/similar_movies?%s' % (movie_id, params)
        logger.debug('Address used for query: %s', url)

        try:
            # send request to api
            request = Request(url, headers=headers)
            json_response = urlopen(request).read()
            logger.debug('Response: %s', json_response)
        except HTTPError:
            logger.error('Invalid API Query.')
            raise
        except URLError:
            logger.error('Network Error. API Query Failed.')
            raise

        data = json.loads(json_response)
        return data