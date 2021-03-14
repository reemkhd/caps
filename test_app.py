import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import os 
from app import create_app
from models import setup_db, Actor, Movie

# Add a new environment variable  
os.environ['assistant_token'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill3cVV5RzlTVmd3ei1FUGRXY1Z0biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcmVlbS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0YWYzYzIzZjY0ODkwMDY4MTkyODA0IiwiYXVkIjoiY2FwIiwiaWF0IjoxNjE1NzE1NDQxLCJleHAiOjE2MTU4MDE0MzMsImF6cCI6Im0yaHJESVpHSHl6Q3ROWTZJR0Vscko4WlBad0pFRzhRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.NmEPM9h9pkwfFvmK06tg6r4nKjb-04uX0RuOypMDcB2q_Rcqk4M93Dr5wgWYMnyYk8QKPSidu_umNYVCW0KhDU-bE26oAJGnDarI9Uc7Pu5VGYUXpJToYtYWmsvAPFhI72ySrKsk-njLijHBdVye2s1h38D2O1b8AR2cDo_1VYAdv5CQO588K2KmdRuvbd1VGtA6YtaVhQuCnTShMifzoTiWvAyGQQnSfg6NYwu_epkrckFewVEWXFfos4joe5ejl3ajSMMGXlM-eyeCAZwJFcFrdi1RZ6F_bSLdeI78Yh5BDTU-6XopS4zwZktdmZfA6664N7-hw1Z-kbvoibtaOg'
os.environ['director_token'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill3cVV5RzlTVmd3ei1FUGRXY1Z0biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcmVlbS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0YjYyM2E1ZDc5NTQwMDcxZGI5MWM5IiwiYXVkIjoiY2FwIiwiaWF0IjoxNjE1NzE1NTQxLCJleHAiOjE2MTU4MDE1MzMsImF6cCI6Im0yaHJESVpHSHl6Q3ROWTZJR0Vscko4WlBad0pFRzhRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.TZEfqE7WbXCO94aj1Zz7uYNcz1aMsgsaeNqT09j8ZjyRMNufmEmbQI0uHx4h-6eUjLiReGpmG-2TtgvyLFwlRNXvEXGsoDmRiYMx6A6idy0DHEgkmbpRqnLcpqWImeGjIJBUafhd_1v6zY6QeofEZZf9DUU2zK-5tjW8g7R8hyY3TkIh-pUAlo446N6zYNi8m6nU0X4ww22DqKrbNYLDI8MM4VQWevAz4fsK-O-5DYkISd4dVc0RWni7tKm67Uh_ExA8-qF0pihnxQ4cMzMPRt3sBuxhE9wgGs-lppY-DcjaxBBQYVEOA5OqWfPP6oIeIKhaaG4t4EcKSvHqvubKtg'
os.environ['producer_token'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill3cVV5RzlTVmd3ei1FUGRXY1Z0biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcmVlbS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0YjY1Mzc5YjFiN2EwMDY5OWQwYzk1IiwiYXVkIjoiY2FwIiwiaWF0IjoxNjE1NzE1NjcyLCJleHAiOjE2MTU4MDE2NjQsImF6cCI6Im0yaHJESVpHSHl6Q3ROWTZJR0Vscko4WlBad0pFRzhRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.GJszAWeW5dVEuxzIMNDElom3cxZ0ZXLSpuf2dxg8a_ls2AI0-_l-rMdxgpQlzptzKWilDN7gijwrobJEnaJgj42dXi5_7GQPZK55tVyaOVFK-fIFA5T56XlTtSJHq2_hyg0UsFLiwJL-9lEp9bvaUZdLudkaCvWgTtNcL92wPdXssHua3SwgamhrzMck9DZ3PR-PZb_x8POKEjnki_f-hoY3hjLIy5j5wNWjw-W1OEArOxscPkgt_2RcFON_6tOSQXVOpbf9n8XjhRPhqcv7wSwsPe4LZ9ngnehHJPiTJreJdLIO4ezhq5OCNm_rNd-_XJAfWQ-OMcVIzKyR8dkDkg'
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
