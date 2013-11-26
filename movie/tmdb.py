from urllib2 import Request, urlopen, URLError, HTTPError
from os.path import expanduser
import json
import logging
from urllib import urlencode
from collections import OrderedDict
from movie import settings

logger = logging.getLogger('root.' + __name__)


class APIException(BaseException):
    pass


class AccessException(BaseException):
    pass


class QueryException(BaseException):
    pass


def get_api_key():
    return settings.api_key


def get_base_url():
    return settings.base_url


def get_details_from_tmdb(movie_id):
    # prepare request to retrieve matching movies for a search term
    logger.info('Searching for details of movie with id %s', movie_id)
    headers = {'Accept': 'application/json'}
    params = {'api_key': settings.api_key, 'movie_id': movie_id}
    url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'.format(**params)
    logger.debug('Address used for query: %s', url)

    try:
        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)
    except HTTPError:
        logger.error('Invalid API Query.')
        raise APIException('Invalid API Query.')
    except URLError:
        logger.error('Network Error. API Query Failed.')
        raise AccessException('Network Error. API Query Failed.')

    data = json.loads(json_response)

    return data


def search_for_movie_by_title(search_term, page):
    # prepare request to retrieve matching movies for a search term
    logger.info('Searching for movie with title %s', search_term)
    headers = {'Accept': 'application/json'}
    params = urlencode(OrderedDict(api_key=settings.api_key, query=search_term, page=page))
    url = 'https://api.themoviedb.org/3/search/movie?%s' % params
    logger.debug('Address used for query: %s', url)

    try:
        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)
    except HTTPError:
        logger.error('Invalid API Query.')
        raise APIException('Invalid API Query.')
    except URLError:
        logger.error('Network Error. API Query Failed.')
        raise AccessException('Network Error. API Query Failed.')

    data = json.loads(json_response)
    return data


# Currently not in use
def get_popular_movies(page):
    # prepare request to retrieve matching movies for a search term
    logger.info('Getting popular movies')
    headers = {'Accept': 'application/json'}
    params = urlencode(OrderedDict(api_key=settings.api_key, page=page))
    url = 'https://api.themoviedb.org/3/movie/popular?%s' % params
    logger.debug('Address used for query: %s', url)

    try:
        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)
    except HTTPError:
        logger.error('Invalid API Query.')
        raise APIException()
    except URLError:
        logger.error('Network Error. API Query Failed.')
        raise AccessException()

    data = json.loads(json_response)
    return data


def get_similar(movie_id, page=1):
    # prepare request to retrieve matching movies for a search term
    logger.info('Getting similar movies to #%s' % movie_id)
    headers = {'Accept': 'application/json'}
    params = urlencode(OrderedDict(api_key=settings.api_key, page=page))
    url = 'https://api.themoviedb.org/3/movie/%s/similar_movies?%s' % (movie_id, params)
    logger.debug('Address used for query: %s', url)

    try:
        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)
    except HTTPError:
        logger.error('Invalid API Query.')
        raise APIException()
    except URLError:
        logger.error('Network Error. API Query Failed.')
        raise AccessException()

    data = json.loads(json_response)
    return data


def get_genre_list():
    # prepare request to retrieve matching movies for a search term
    logger.info('Getting genre list')
    headers = {'Accept': 'application/json'}
    params = urlencode(OrderedDict(api_key=settings.api_key))
    url = 'https://api.themoviedb.org/3/genre/list?%s' % params
    logger.debug('Address used for query: %s', url)

    try:
        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)
    except HTTPError:
        logger.error('Invalid API Query.')
        raise APIException()
    except URLError:
        logger.error('Network Error. API Query Failed.')
        raise AccessException()

    data = [(s['id'], s['name']) for s in json.loads(json_response)['genres']]
    return data


def get_movies_for_genre(genre_id, page=1):
    # prepare request to retrieve matching movies for a search term
    logger.info('Getting movies for genre #%s' % genre_id)
    headers = {'Accept': 'application/json'}
    params = urlencode(OrderedDict(api_key=settings.api_key, page=page))
    if genre_id:
        url = 'https://api.themoviedb.org/3/genre/%s/movies?%s' % (genre_id, params)
    else:
        url = 'https://api.themoviedb.org/3/discover/movie?%s' % params
    logger.debug('Address used for query: %s', url)

    try:
        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)
    except HTTPError:
        logger.error('Invalid API Query.')
        raise APIException()
    except URLError:
        logger.error('Network Error. API Query Failed.')
        raise AccessException()

    data = json.loads(json_response)
    return data