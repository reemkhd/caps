import os
from flask import (Flask, request, abort,
                   jsonify, render_template, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.config['SECRET_KEY'] = 'any secret string'

    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route("/", methods=['GET'])
    def home():
        msg = 'Welcome to Casting Agency API'
        return jsonify(msg)

    @app.route("/movies", methods=['GET'])
    @requires_auth("get:movies")
    def movie(jwt):
        #Get all movies from db
        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def actors(jwt):
        #Get all actors from db
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def insert_movie(jwt):
        # take the data that the user fill it
        body = request.get_json()
        # there is an error when the user don't write the name or date
        if not ('name' in body and 'relase_date' in body):
            abort(422)
        else:
            try:
                movie = Movie(
                    name=body['name'],
                    relase_date=body['relase_date'])
                actor_id = Actor.query.filter(
                    Actor.id == body['actor_id']).one_or_none()
                movie.actor = [actor_id]
                #insert the movie data into db
                movie.insert()
                return jsonify({
                    'success': True,
                    'movie': movie.format()
                })
            except BaseException:
                abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def insert_actor(jwt):
        body = request.get_json()
        # there is an error when the user don't write the name
        if not ('name' in body):
            abort(422)
        else:
            try:
                actor = Actor(
                    name=body['name'],
                    age=body['age'],
                    gendar=body['gendar'])
                movies = Movie.query.filter(
                    Movie.id == body['movies']).one_or_none()
                actor.movies = [movies]
                #insert the actor data into db
                actor.insert()
                return jsonify({
                    'success': True,
                    'actor': actor.format()
                })
            except BaseException:
                abort(404)

    @app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
    @requires_auth('patch:movie')
    def edit_movie(jwt, movie_id):
        # take the ID of the movie that want to edit
        movie = Movie.query.get(movie_id)
        if movie:
            body = request.get_json()
            #if the name is updated, update the movie in db
            if 'name' in body:
                movie.name = body['name']
            #if the date is updated, update the movie in db
            if 'relase_date' in body:
                movie.relase_date = body['relase_date']
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })

    @app.route('/actors/<int:actor_id>/edit', methods=['PATCH'])
    @requires_auth('patch:actor')
    def edit_actor(jwt, actor_id):
        # take the ID of the actor that want to edit
        actor = Actor.query.get(actor_id)
        if actor:
            body = request.get_json()
            #if the name is updated, update the actor in db
            if 'name' in body:
                actor.name = body['name']
            #if the age is updated, update the actor in db
            if 'age' in body:
                actor.age = body['age']
            #if the dendar is updated, update the actor in db
            if 'gendar' in body:
                actor.gendar = body['gendar']
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })

    @app.route('/movies/<int:movie_id>/delete', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        # take the id thats want to delete
        movie = Movie.query.get(movie_id)
        #try to delete the movie
        try:
            movie.delete()
        #if there is error, don't change the db
        except BaseException:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    @app.route('/actors/<int:actor_id>/delete', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, actor_id):
        # take the id thats want to delete
        actor = Actor.query.get(actor_id)
        #try to delete the actor
        try:
            actor.delete()
        #if there is error, don't change the db
        except BaseException:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })


    # error handlers for all expected errors
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Permission not found"
        }), 401

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def unauthorized(error):
        print(error.status_code)
        print(error.error)
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
