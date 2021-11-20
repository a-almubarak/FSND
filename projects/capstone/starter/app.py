import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_create_all, Movie, Actor



# create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)

db_create_all()

@app.route('/movies',methods=['GET'])
def get_movies():
    pass

@app.route('/movies',methods=['POST'])
def post_movies():
    pass

@app.route('/movies/<int:movie_id>',methods=['PATCH'])
def patch_movies(movie_id):
    pass

@app.route('/movies/<int:movie_id>',methods=['DELETE'])
def delete_movies(movie_id):
    pass

@app.route('/actors',methods=['GET'])
def get_actors():
    pass

@app.route('/actors',methods=['POST'])
def post_actors():
    pass

@app.route('/actors/<int:actor_id>',methods=['PATCH'])
def patch_actors(actor_id):
    pass

@app.route('/actors/<int:actor_id>',methods=['DELETE'])
def delete_actors(actor_id):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
