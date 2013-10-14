from urllib2 import Request, urlopen, URLError
from os.path import expanduser
import os.path
import json
import logging

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
                raise Exception('Please ensure that a file with the API key exists in the directory %s' % path)
            except:
                raise Exception('Could not access API Key at path %s' % path)

            logger.debug('Using API Key: %s', Tmdb.api_key)
            return Tmdb.api_key

    @staticmethod
    def get_base_url():
        """
        Get base url for Tmdb images.
        """
        if not Tmdb.base_url:
            # get base url from web service
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
                raise Exception('Network Error. API Query Failed.')
            except:
                raise Exception('Error retrieving base_url.')
        return Tmdb.base_url

    @staticmethod
    def get_details_from_tmdb(movie_id):
        # prepare request to retrieve matching movies for a search term
        headers = {'Accept': 'application/json'}
        params = {'api_key': Tmdb.get_api_key(), 'movie_id': movie_id}
        url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'.format(**params)
        logger.debug('Address used for query: %s', url)

        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)

        data = json.loads(json_response)
        return data

    @staticmethod
    def search_for_movie_by_title(search_term):
        # prepare request to retrieve matching movies for a search term
        headers = {'Accept': 'application/json'}
        params = {'api_key': Tmdb.get_api_key(), 'search_term': search_term}
        url = 'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={search_term}'.format(**params)
        logger.debug('Address used for query: %s', url)

        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
        logger.debug('Response: %s', json_response)

        data = json.loads(json_response)
        return data