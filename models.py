from sqlalchemy import Column, Integer, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
from sqlalchemy import DateTime
from dataclasses import dataclass

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://qdtbedjanjtobz:89028659959d448deb1c200e2016025978ac72868430133949bb0face67e6fb0@ec2-54-145-249-177.compute-1.amazonaws.com:5432/deue955r2tp1cc'    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()

# For many-to-many relationship between Movie & Actor
# the Movie table is the parent since it is more important
actor_movie = db.Table(
    'actor_movie',
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('actor.id'),
        primary_key=True),
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movie.id'),
        primary_key=True))


'''
Extend the base Model class to add common methods
'''
class inheritedClassName(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


@dataclass
class Movie(inheritedClassName):
    id: int
    name: String
    relase_date: DateTime

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    relase_date = db.Column(DateTime)

    def __init__(self, relase_date, name):
        self.relase_date = relase_date
        self.name = name

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'relase_date': self.relase_date,
            'actors': [x.name for x in self.actor]
        }

@dataclass
class Actor(inheritedClassName):
    id: int
    name: String
    age: int
    gendar: String
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gendar = db.Column(db.String)

    movies = db.relationship('Movie', secondary=actor_movie, lazy='subquery',
                             backref=db.backref('actor', lazy=True))

    def __init__(self, name, age, gendar):
        self.age = age
        self.gendar = gendar
        self.name = name

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gendar': self.gendar,
            'movies': [x.name for x in self.movies]
        }
