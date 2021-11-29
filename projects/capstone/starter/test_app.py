import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db

class CapstoneTestClass(unittest.TestCase):

    def setup(self):
        self.app = app
        self.client = self.app.test_client
        self.db_host = os.getenv('DB_HOST','localhost:5432')
        self.db_user = os.getenv('DB_USER','postgres')
        self.db_password = os.getenv('DB_PASSWORD','123123')
        self.database_name = 'capstone_test'
        self.database_path = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.database_name}'
        setup_db(self.app,self.database_path)
       # binds the app to the current context 
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    

    

