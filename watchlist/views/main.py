from flask import Blueprint, render_template, request, current_app, redirect, flash
from flask_login import current_user, login_required

from tmdb_api import WatchlistAPI
from watchlist.extensions import db
from watchlist.models import MovieWatchlist

routes = Blueprint('main', __name__)


def get_watchlist_api() -> WatchlistAPI:
    tmdb_api_key = current_app.config['TMDB_API_KEY']
    return WatchlistAPI(tmdb_api_key)


@routes.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        watchlist = get_watchlist_api()

        user_movies_watchlist = current_user.movies_watchlist
        movies = list()
        for user_movie in user_movies_watchlist:
            movie = watchlist.movie.search_by_id(user_movie.movie_id)
            movie.in_watchlist = True
            movies.append(movie)

        return render_template('main/index.html', movies=movies)
    return render_template('main/index.html')


# @routes.route('/search', methods=['GET'])
# def search():
#     return render_template('main/search.html')


@routes.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')

    watchlist = get_watchlist_api()

    if query:
        movies = watchlist.movie.search(query)
    else:
        movies = list()

    if current_user.is_authenticated:
        user_movies_watchlist = current_user.movies_watchlist
        for user_movie in user_movies_watchlist:
            for movie in movies:
                if user_movie.movie_id == movie.id:
                    movie.in_watchlist = True

    return render_template('main/search.html', movies=movies)


@routes.route('/add_to_watchlist', methods=['GET'])
@login_required
def add_to_watchlist():
    movie_id = request.args.get('movie_id')
    url = request.referrer

    movie = MovieWatchlist(movie_id=movie_id, user_id=current_user.id)
    db.session.add(movie)
    db.session.commit()

    return redirect(url + f'#{movie_id}')


@routes.route('/remove_from_watchlist', methods=['GET'])
@login_required
def remove_from_watchlist():
    movie_id = int(request.args.get('movie_id'))
    url = request.referrer

    if current_user.is_authenticated:
        user_movies_watchlist = current_user.movies_watchlist
        watchlist = get_watchlist_api()

        for user_movie in user_movies_watchlist:
            if user_movie.movie_id == movie_id:
                db.session.delete(user_movie)
                db.session.commit()
                movie = watchlist.movie.search_by_id(movie_id)
                flash(f'Removed {movie.title}', 'alert-success')

    return redirect(url + f'#{movie_id}')
