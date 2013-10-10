# TMDB Example
# Author: Matt Meisinger
#
# This is a script to test the connection to the TMDB.  It assumes you have the TMDB API key saved
# in a file named ~/.tmdb_api_key on your local filesystem.  It will search for movies matching a search 
# term and return json.

from urllib2 import Request, urlopen
from os.path import expanduser

# read API key
with open(expanduser('~/.tmdb_api_key'), 'r') as f:
	apikey = f.read().replace('\n','')
print 'Using API Key: ' + apikey

# prepare request to retrieve matching movies for a search term
search_term = 'fire'
headers = {"Accept": "application/json"}
url = "http://api.themoviedb.org/3/search/movie?api_key={apikey}&query={query}".format(apikey=apikey,query=search_term)
print url

# send request to api
request = Request(url, headers=headers)
json_response = urlopen(request).read()
print json_response