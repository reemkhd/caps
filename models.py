from sqlalchemy import Column, Integer, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
from sqlalchemy import DateTime


database_name = "cap"
user_name = "reem"
password = ""
database_path = "postgresql://{}:{}@{}/{}".format(
  user_name,
  password,
  'localhost:5432',
  database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()


# For many-to-many relationship between Movie & Actor
# the Movie table is the parent since it is more important
actor_movie = db.Table('actor_movie',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
)


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    relase_date = db.Column(DateTime)


    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'relase_date': self.relase_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gendar = db.Column(db.String)

    movie_id = db.relationship('Movie', secondary=actor_movie, lazy='subquery',
        backref=db.backref('actor', lazy=True))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gendar': self.gendar
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()