import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import os 
from app import create_app
from models import setup_db, Actor, Movie

# Add a new environment variable  
os.environ['assistant_token'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill3cVV5RzlTVmd3ei1FUGRXY1Z0biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcmVlbS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0YWYzYzIzZjY0ODkwMDY4MTkyODA0IiwiYXVkIjoiY2FwIiwiaWF0IjoxNjE1NTc1NDQzLCJleHAiOjE2MTU2NDc0NDMsImF6cCI6Im0yaHJESVpHSHl6Q3ROWTZJR0Vscko4WlBad0pFRzhRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.SYriiU1HdHQjhTqLZqKgmaAA-00JYWjACsr_EElRlwER-GuW5R9xq1b5b_mqyF3lS7z8eQ4wTgCv5ylNz4y7DViHVGm5QbEku4c7aQP441ScYYKesYtXT7YEneAJni_gvWY9wsWguMVq_00wZMi-1z_L06Wu0GkRr1Qrgea1SCjE77jP6Wzd3ffMLFBequs5UwbE3f_jg55y8rRNxYlO0DTvq-qhlZaGZeJRvhShg3Qh58wz8GIM6XIOrBQjLVaLCCVg7WJsjYRJnypCup_6EXWsBpNT301Xz6QXvet7-ohk2G-HMbMhavYtyusgeYbvU86Xexj9Ezs1F28npt30Kg'
os.environ['director_token'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill3cVV5RzlTVmd3ei1FUGRXY1Z0biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcmVlbS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0YjYyM2E1ZDc5NTQwMDcxZGI5MWM5IiwiYXVkIjoiY2FwIiwiaWF0IjoxNjE1NTc1Mzg1LCJleHAiOjE2MTU2NDczODUsImF6cCI6Im0yaHJESVpHSHl6Q3ROWTZJR0Vscko4WlBad0pFRzhRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.LivIRU3ftiiXVhO1Ku2l9wxEMpSYRhI0ZDCR-_Q9nZATrGJQNizR6lanTkyUO2EkmoHWhSOU-ewYUrQc03aKUgpIzfuixLCUIOW8cfgDM3E0Gl8bAbO1FBW_hdBVi1BBMqCEtmSTzp4XXDRRGNhPcA0yIbx94qSwTyQS7NJhfp1NvdlRIsKQGInxIllAUVVFaUlh0fJZSy_CYDJdzvLfaC9EXy06hkO0981-ptD2R2HHOC7kWbyOuXhs79_Ybf9ykIMd0hACDJILBA0_eqoxbhLjWn-aJ82us-RsidLg1UdaP4CNcd5WcZ_--ePx9FnqcT_ZosNdOzXt_WIRXc6Zbw'
os.environ['producer_token'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill3cVV5RzlTVmd3ei1FUGRXY1Z0biJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcmVlbS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0YjY1Mzc5YjFiN2EwMDY5OWQwYzk1IiwiYXVkIjoiY2FwIiwiaWF0IjoxNjE1NTc1MzE5LCJleHAiOjE2MTU2NDczMTksImF6cCI6Im0yaHJESVpHSHl6Q3ROWTZJR0Vscko4WlBad0pFRzhRIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.dU0cEa6q-9mlSFg6uRLjsZrG5Zo1s5wPYq1mGymK5WJl_yl4ungLHTf5-V0gIPDKkxpNWhNWr8jO5w-dici7r4gu8zsFAb4gpdPyWEFZgDu7ydGeh-9RVaN8KwnPmXVU_5A0fCK00eYtTvx0vahEP-6AZPRqYIao5SVnqWMW_HNEzAAsUCqcC5r4MsDAY3rJuU8I9SxEW2J7mIXOKJo20hQuaG9qGafQvC6p_W0pRmdv7Zao8M1_OUVYXawyd4ha28nJp1v-WSLRJEVyKrqykc8f7t2rb4NlLicsBuELQHyGgyw-q9IUYR_huY6Hy2zyjwcgryLumjI3ntxerhlLkA'
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
