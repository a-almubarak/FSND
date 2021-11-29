import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import requires_auth, AuthError
from sqlalchemy.exc import IntegrityError

nbActors = 10
nbMovies = 10

# create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','POST,GET,PATCH,DELETE')
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
@requires_auth('get:movies')
def get_movies():
    movies = Movie.query.all()
    data = paginated_movies(request,movies)
    return jsonify({
        # 'success':True,
        'movies':data
    })

@app.route('/movies',methods=['POST'])
@requires_auth('post:movies')
def post_movies():
    body = request.get_json()
    if ('title' in body) and ('release_date' in body):
        title = body['title']
        release_date = body['release_date']
        tmp = Movie(title=title,release_date=release_date) 
        tmp.insert()
        return jsonify({
            # 'success':True,
            'id':tmp.id
        })
    else:
        abort(400)

@app.route('/movies/<int:movie_id>',methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movies(movie_id):
    movie = Movie.query.get(movie_id)
    body = request.get_json()
    if not movie:
        abort(404)
    if 'title' in body:
        movie.title = body['title']
    if 'release_date' in body:
        movie.release_date = body['release_date']
    if 'actors' in body:
        for actor in body['actors']:
            movie.actors.append(Actor.query.get_or_404(actor['actor_id']))
    movie.update()
    return jsonify({
        # 'success':True,
        'id':movie_id
    })

@app.route('/movies/<int:movie_id>',methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    movie.delete()
    return jsonify({
        # 'success':True,
        'id':movie_id
    })

#------------------------------------------------------------

# --- Actor ------------------------------------------------
@app.route('/actors',methods=['GET'])
@requires_auth('get:actors')
def get_actors():
    actors = Actor.query.all()
    data = paginated_actors(request,actors)
    return jsonify({
        # 'success':True,
        'actors':data
    })

@app.route('/actors',methods=['POST'])
@requires_auth('post:actors')
def post_actors():
    body = request.get_json()
    if 'name' in body and 'age' in body and 'gender' in body:
        actor = Actor(name=body['name'],age=body['age'],gender=body['gender'])
        actor.insert()
        return jsonify({
            # 'success':True,
            'id':actor.id
        })
    else:
        abort(400)

@app.route('/actors/<int:actor_id>',methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actors(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)
    
    body = request.get_json()
    if 'name' in body:
        actor.name = body['name']
    if 'age' in body:
        actor.age = body['age']
    if 'movies' in body:
        for movie in body['movies']:
            actor.movies.append(Movie.query.get_or_404(movie['movie_id']))
    
    actor.update()
    return jsonify({
        # 'success':True,
        'id':actor.id
    })

@app.route('/actors/<int:actor_id>',methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)
    actor.delete()
    return jsonify({
        # 'success':True,
        'id':actor_id
    })

#------------------------------------------------------------
#------  Error Handlers -------------------------------------

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        # 'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        # 'success': False,
        'error': 404,
        'message': 'not found'
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        # 'success': False,
        'error': 422,
        'message': 'unprocessable',
    }), 422

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        # 'success': False,
        'error': 500,
        'message': 'internal error'
    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response

@app.errorhandler(IntegrityError)
def integrity_error(error):
    db.session.rollback()
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
    
#------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
