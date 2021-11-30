import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from app.models import setup_db


def auth_header(token):
    return {'Authorization': f'Bearer {token}'}


def movie_body(title, release_date):
    return {
        'title': title,
        'release_date': release_date
    }


def actor_body(name, age, gender):
    return {
        'name': name,
        'age': age,
        'gender': gender
    }
casting_assistant = auth_header(os.getenv('casing_assistant'))
casting_director = auth_header(os.getenv('casting_director'))
executive_producer = auth_header(os.getenv('executive_producer'))

class CapstoneTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.db_host = os.getenv('DB_HOST', 'localhost:5432')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', '123123')
        self.database_name = 'capstone_test'
        self.database_path = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.database_name}'
        setup_db(self.app, self.database_path)
       # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_get_movies_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_get_movies_200(self):
        res = self.client().get('/movies', headers=auth_header(os.getenv('casting_assistant')))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # there is no movies in the beginning
        self.assertTrue(data['movies'])

    def test_post_movies_403(self):
        res = self.client().post('/movies', json=movie_body('Batman vs Superman', '2015'),
                                 headers=auth_header(os.getenv('casting_assistant')))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unprocessable')

    def test_post_movies_200(self):
        res = self.client().post('/movies',json=movie_body('Batman vs Superman','2015'),headers=auth_header(os.getenv('executive_producer')))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['id'])

    def test_post_movies_400(self):
        res = self.client().post('/movies',json={'title':'Test'},headers=auth_header(os.getenv('executive_producer')))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'],'bad request')


    def test_delete_movies_404(self):
        res = self.client().delete('/movies/0',headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'not found')
    
    def test_delete_movies_200(self):
        res = self.client().delete('/movies/6',headers=executive_producer)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['id'],6)
    
    def test_patch_movies_404(self):
        res = self.client().patch('/movies/0',headers=executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'not found')

    def test_patch_movies_200(self):
        res = self.client().patch('/movies/5',headers=executive_producer,json={'title':'You'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['id'])

#--- Actor test cases -----------------------------------------
    def test_get_actors_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_get_actors_200(self):
        res = self.client().get('/actors', headers=auth_header(os.getenv('casting_assistant')))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # there is no actors in the beginning
        self.assertTrue(data['actors'])

    def test_post_actors_403(self):
        res = self.client().post('/actors', json=actor_body('Bryan Cranston', '62','M'),
                                 headers=auth_header(os.getenv('casting_assistant')))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unprocessable')

    def test_post_actors_200(self):
        res = self.client().post('/actors',json=actor_body('Bryan Cranston','62','M'),headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['id'])

    def test_post_actors_400(self):
        res = self.client().post('/actors',json={'name':'Test'},headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'],'bad request')


    def test_delete_actors_404(self):
        res = self.client().delete('/actors/0',headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'not found')
    
    def test_delete_actors_200(self):
        res = self.client().delete('/actors/1',headers=casting_director)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['id'],1)
    
    def test_patch_actors_404(self):
        res = self.client().patch('/actors/0',headers=casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'not found')

    def test_patch_actors_200(self):
        res = self.client().patch('/actors/2',headers=casting_director,json={'name':'You'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['id'])


if __name__ == '__main__':
    unittest.main()
