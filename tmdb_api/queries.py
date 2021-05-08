from abc import ABC, abstractmethod
from typing import List, Union

from tmdb_api.schemas import TV, Movie


class Base(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def search(self, query: str):
        pass


class QueryTV(Base):
    def __init__(self, query):
        super().__init__()
        self.__tv = query

    def search(self, query: str) -> List[TV]:
        result = self.__tv.search(query)
        return [TV(**tv) for tv in result]


class QueryMovie(Base):
    def __init__(self, query):
        super().__init__()
        self.__movie = query

    def search(self, query: str) -> List[Movie]:
        result = self.__movie.search(query)
        return [Movie(**movie) for movie in result]

    def search_by_id(self, id: Union[str, int]):
        result = self.__movie.details(int(id))
        return Movie(**result)
