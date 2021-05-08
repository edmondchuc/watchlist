from flask_login import UserMixin

from watchlist.extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(100))

    movies_watchlist = db.relationship('MovieWatchlist', backref='user')

    def __repr__(self):
        return f'<User {self.username}'


class MovieWatchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<MovieWatchlist {self.title}'
