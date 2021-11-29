import os
from flask_sqlalchemy import SQLAlchemy

db_host = os.getenv('DB_HOST','localhost:5432')
db_user = os.getenv('DB_USER','postgres')
db_password = os.getenv('DB_PASSWORD','123123')
database_name = 'capstone'
database_path = f'postgresql://{db_user}:{db_password}@{db_host}/{database_name}'

db = SQLAlchemy()

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    

association_table = db.Table('association',db.Model.metadata,
                            db.Column('movie_id',db.Integer,db.ForeignKey('movie.id'),primary_key=True),
                            db.Column('actor_id',db.Integer,db.ForeignKey('actor.id'),primary_key=True))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    actors = db.relationship("Actor",secondary=association_table,lazy='subquery',backref=db.backref('movies',lazy=True))

    def format(self):
        return ({
            'id':self.id,
            'title':self.title,
            'release_date':self.release_date,
            'actors':[{'actor_id' : i.id for i in self.actors}]
        })
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def format(self):
        return ({
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'gender':self.gender,
            'movies':[{'movie_id' : i.id for i in self.movies}]
        })
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

