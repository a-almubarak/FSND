import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

database_path = ''

db = SQLAlchemy()

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    
def db_create_all():
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
        return jsonify({
            'id':self.id,
            'title':self.title,
            'release_date':self.release_date,
            'actors':[i.id for i in self.actors]
        })

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def format(self):
        return jsonify({
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'gender':self.gender,
            'movies':[i.id for i in self.movies]
        })

