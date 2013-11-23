from ase1.models import Movie
import logging

logger = logging.getLogger('root.' + __name__)


# An attribute by which to filter the displayed movies
# Each entry of browse_filters must contain a 'name' field and an 'option_list'
class BrowseFilter(object):
    def __init__(self, name):
        self.name = name
        self.option_list = []


# Each attribute value is represented as a FilterElement.
# id_ is passed into the GET request
# name describes the attribute value for the user
class FilterElement(object):
    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name


def get_browse_filters():
    logger.info('Retrieving Browse Filters')
    # A list of attributes by which the user can filter the displayed movies
    browse_filters = []

    # Create the Genre filter
    genre_filter = BrowseFilter('genre')

    # Add default option. Not filtered by Genre
    default_option = FilterElement('', 'All')
    genre_filter.option_list.append(default_option)

    # Retrieve list of genres from API
    logger.info('Retrieving Genre List')
    retrieved_genres = Movie.get_genres()
    # Add retrieved genres to list as Genre objects
    for id_, name in retrieved_genres:
        genre = FilterElement(id_, name)
        genre_filter.option_list.append(genre)
    if not retrieved_genres:
        logger.warning('No Genres Retrieved')

    browse_filters.append(genre_filter)

    logger.info('Finished Retrieving Browse Filters')
    return browse_filters
