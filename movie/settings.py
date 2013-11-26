from urllib2 import Request, urlopen, URLError
import json
import logging

logger = logging.getLogger('root.' + __name__)


# Get base url for Tmdb images. If this cannot access the API at build time,
# the Exception will be uncaught and the build will terminate
def __gen_base_url():
    # get base url from web service
    logger.info('Retrieving base url')
    headers = {'Accept': 'application/json'}
    params = {'api_key': api_key}
    url = 'https://api.themoviedb.org/3/configuration?api_key={api_key}'.format(**params)
    logger.debug('Address used for query: %s', url)

    try:
        # send request to api
        request = Request(url, headers=headers)
        json_response = urlopen(request).read()
    except URLError:
        logger.error('Network Error. API Query Failed.')
        raise
    data = json.loads(json_response)
    new_base_url = data['images']['base_url']
    logger.debug('Base URL: %s', new_base_url)
    return new_base_url

# The api key to use for the TMDB to work.  This needs to be set before the
# application can work.
api_key = 'f93d4374e57a40fd7cc1028e0c95ad9f'

# This is only necessary if implementation changes
#if not api_key:
#    raise Exception('Unable to find API key in "/movie/settings.py".\
# An account must be created and a TMDB API key acquired before this application can run.')

# The base url for TMDB images
base_url = __gen_base_url()
