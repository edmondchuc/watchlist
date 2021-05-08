from datetime import date

from pydantic import BaseModel


class TV(BaseModel):
    id: int
    name: str
    overview: str = None
    first_air_date: str = None
    poster_path: str = None
    vote_average: float = None
    vote_count: int = None


class Movie(BaseModel):
    id: int
    title: str
    overview: str = None
    release_date: str = None
    poster_path: str = None
    vote_average: float = None
    vote_count: int = None
    in_watchlist: bool = False
    in_watched: bool = False
