import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import os 
from app import create_app
from models import setup_db, Actor, Movie

class CapstoneTest(unittest.TestCase):
    
    def setUp(self):
        self.token_assistant = os.environ['assistant_token']
        self.token_director = os.environ['director_token']
        self.token_producer = os.environ['producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

#------------ Test Actors endpoint
    def test_get_Actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": 'bearer '+ self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    def test_get_Actors_fail(self):
        res = self.client().get('/act', headers={
            "Authorization": 'bearer '+ self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    def test_get_Actors_fail_unauthorized(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)


    def test_create_Actor(self):
        res = self.client().post(
            '/actors',
            json={
                "name" : "yakml",
                "age" : 12,
                "gendar" : "male",
                "movie_id" : 8
            },
            headers={"Authorization": 'bearer ' + self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    def test_create_Actor_fail(self):
        res = self.client().post(
            '/actors',
            json={
                "name" : "yakml",
                "age" : 12,
                "movie_id" : 8
            },
            headers={"Authorization": 'bearer ' + self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    def test_create_Actor_fail_unauthorized(self):
        res = self.client().post(
            '/actors',
            json={
                "name" : "yakml",
                "age" : 12,
                "movie_id" : 8
            },
            headers={"Authorization": 'bearer ' + self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)


    def test_edit_Actor(self):
        res = self.client().patch(
            '/actors/8/edit',
            json={
                "name" : "lolo-dkh",
                "age" : 55,
                "gendar" : "female",
                "movie_id" : 13
            },
            headers={"Authorization": 'bearer ' + self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    def test_edit_Actor_fail(self):
        res = self.client().patch(
            '/actors/8/',
            json={
                "name" : "lolo-dkh",
                "age" : 55,
                "gendar" : "female",
                "movie_id" : 13
            },
            headers={"Authorization": 'bearer ' + self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    def test_edit_Actor_fail_unauthorized(self):
        res = self.client().patch(
            '/actors/8/',
            json={
                "name" : "lolo-dkh",
                "age" : 55,
                "gendar" : "female",
                "movie_id" : 13
            },
            headers={"Authorization": 'bearer ' + self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)


    def test_delete_Actors(self):
        res = self.client().delete('/actors/7/delete', headers={
            "Authorization": 'bearer '+ self.token_producer})
        body = json.loads(res.data)
        ques = Actor.query.filter_by(id=7).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(ques, None)
    def test_delete_Actors_fail(self):
        res = self.client().delete('/actors/8/', headers={
            "Authorization": 'bearer '+ self.token_producer})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)



#------------ Test Movies endpoint
    def test_get_Movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'bearer '+ self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    def test_get_Movies_fail(self):
        res = self.client().get('/mov', headers={
            "Authorization": 'bearer '+ self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    def test_get_Movies_fail_unauthorized(self):
        res = self.client().get('/movies')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)


    def test_create_Movie(self):
        res = self.client().post(
            '/movies',
            json={
                "name" : "blue eyes",
                "relase_date" : "2021-03-09 21:45:07",
                "actor_id" : 6
            },
            headers={"Authorization": 'bearer ' + self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    def test_create_Movie_fail(self):
        res = self.client().post(
            '/mov',
            json={
                "name" : "blue eyes",
                "relase_date" : "2021-03-09 21:45:07",
                "actor_id" : 6
            },
            headers={"Authorization": 'bearer ' + self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    def test_create_Movie_fail_unauthorized(self):
        res = self.client().post(
            '/movies',
            json={
                "name" : "blue eyes",
                "relase_date" : "2021-03-09 21:45:07",
                "actor_id" : 6
            },
            headers={"Authorization": 'bearer ' + self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)
        

    def test_edit_Movie(self):
        res = self.client().patch(
            '/movies/40/edit',
            json={
                "name" : "blue eyes",
                "relase_date" : "2020-03-09 21:45:07",
                "actor_id" : 6
            },
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
    def test_edit_Movie_fail(self):
        res = self.client().patch(
            '/movies/8/',
            json={
                "name" : "blue eyes",
                "relase_date" : "2021-03-09 21:45:07",
                "actor_id" : 6
            },
            headers={"Authorization": 'bearer ' + self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)


    def test_delete_Movie(self):
        res = self.client().delete('/movies/9/delete', headers={
            "Authorization": 'bearer '+ self.token_producer})
        body = json.loads(res.data)
        ques = Movie.query.filter_by(id=7).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(ques, None)
    def test_delete_Movie_fail(self):
        res = self.client().delete('/movies/10/', headers={
            "Authorization": 'bearer '+ self.token_producer})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)
    def test_delete_Movie_fail_unauthorized(self):
        res = self.client().delete('/movies/10/delete', headers={
            "Authorization": 'bearer '+ self.token_director})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

if __name__ == '__main__':
    unittest.main()
