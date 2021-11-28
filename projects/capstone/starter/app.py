import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

nbActors = 10
nbMovies = 10

# create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.add('Access-Control-Allow-Methods','POST,GET,PATCH,DELETE')
    return response


# -----   Helping methods -----------------------------
def paginated_movies(request,selection):
    page = request.args.get('page',1)
    start = (page-1)*nbMovies
    end = start + nbMovies
    data = [select.format() for select in selection]
    return data[start:end]

def paginated_actors(request,selection):
    page = request.args.get('page',1)
    start = (page-1)*nbActors
    end = start + nbActors
    data = [select.format() for select in selection]
    return data[start:end]
#------------------------------------------------------------

# --- Movies ------------------------------------------------
@app.route('/movies',methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    data = paginated_movies(request,movies)
    return jsonify({
        'success':True,
        'movies':data
    })

@app.route('/movies',methods=['POST'])
def post_movies():
    body = request.get_json()
    if ('title' in body) and ('release_date' in body):
        title = body['title']
        release_date = body['release_date']
        tmp = Movie(title=title,release_date=release_date) 
        return jsonify({
            'success':True,
            'id':tmp.id
        })
    else:
        abort(400)

@app.route('/movies/<int:movie_id>',methods=['PATCH'])
def patch_movies(movie_id):
    movie = Movie.query.get(movie_id).one_or_none()
    body = request.get_json()
    if not movie:
        abort(404)
    if 'title' in body:
        movie.title = body['title']
    if 'release_date' in body:
        movie.release_date = body['release_date']
    if 'actors' in body:
        movie.actors.append(body['actors'])
    movie.update()
    return jsonify({
        'success':True,
        'id':movie_id
    })

@app.route('/movies/<int:movie_id>',methods=['DELETE'])
def delete_movies(movie_id):
    movie = Movie.query.get(movie_id).one_or_none()
    if not movie:
        abort(404)
    movie.delete()
    return jsonify({
        'success':True,
        'id':movie_id
    })

#------------------------------------------------------------

# --- Actor ------------------------------------------------
@app.route('/actors',methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    data = paginated_actors(request,actors)
    return jsonify({
        'success':True,
        'actors':data
    })

@app.route('/actors',methods=['POST'])
def post_actors():
    body = request.get_json()
    if 'name' in body and 'age' in body and 'gender' in body:
        actor = Actor(name=body['name'],age=body['age'],gender=body['gender'])
        actor.insert()
        return jsonify({
            'success':True,
            'id':actor.id
        })
    else:
        abort(400)

@app.route('/actors/<int:actor_id>',methods=['PATCH'])
def patch_actors(actor_id):
    actor = Actor.query.get(actor_id).one_or_none()
    if not actor:
        abort(404)
    
    body = request.get_json()
    if 'name' in body:
        actor.name = body['name']
    if 'age' in body:
        actor.age = body['age']
    if 'movies' in body:
        actor.movies.append(body['movies']) 
    
    actor.update()
    return jsonify({
        'success':True,
        'id':actor.id
    })

@app.route('/actors/<int:actor_id>',methods=['DELETE'])
def delete_actors(actor_id):
    actor = Actor.query.get(actor_id).one_or_none()
    if not actor:
        abort(404)
    actor.delete()
    return jsonify({
        'success':True,
        'id':actor_id
    })

#------------------------------------------------------------
#------  Error Handlers -------------------------------------

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'not found'
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable',
    }), 422

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal error'
    }), 500

#------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
