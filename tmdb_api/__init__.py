from tmdbv3api import TMDb, Movie, TV

from tmdb_api.queries import QueryTV, QueryMovie


class WatchlistAPI:
    def __init__(self, api_key: str, language: str = 'en'):
        self.tmbd = TMDb()
        self.tmbd.api_key = api_key
        self.tmbd.language = language

        self.__tv = QueryTV(TV())
        self.__movie = QueryMovie(Movie())

    @property
    def tv(self):
        return self.__tv

    @property
    def movie(self):
        return self.__movie
