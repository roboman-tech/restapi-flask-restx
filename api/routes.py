from flask import  request, jsonify
from flask_restx import  Resource
from api.restx_model import api, movie_model
from api.models import db
from sqlalchemy.exc import IntegrityError

from api.models import Movies

@api.route('/movies')
class Movie(Resource):
    @api.expect(movie_model, code=200)
    @api.response(409, "Movie already exists")
    @api.response(500, 'Internal Server Error')
    @api.response(200, 'Success')
    def post(self):
        ''' Post a new movie '''
        try:
            payload = request.get_json()
            title = payload["title"]
            genre = payload["genre"]
            release_year = payload["release_year"]

            new_movie = Movies(title=title, release_year=release_year, genre=genre)
            db.session.add(new_movie)

            db.session.commit()
            return jsonify(new_movie.to_dict)
        except IntegrityError:
            db.session.rollback()
            api.abort(409, "Movie with the given title already exists")
        except Exception as e:
            api.abort(500, f"Internal Server Error: {str(e)}")

@api.route('/movies/<int:id>')
class MovieResource(Resource):

    @api.response(404, 'Move not Found')
    @api.response(200, 'Success', movie_model)
    @api.response(500, 'Internal Server Error')
    def get(self, id):
        ''' Get a movie by ID '''
        try:
            movie = Movies.query.get(id)
            if movie:
                return jsonify(movie.to_dict)
            else:
                return {"message": "The movie you are looking for is not found", "type": "error"}, 404
        except Exception as e:
            print(f"Exception occurred: {e}")
            api.abort(500, message="Internal Server Error", type="error")

    @api.response(404, 'Movie not Found')
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    @api.expect(movie_model, code=200)
    def put(self, id):
        ''' Update a movie '''
        try:
            movie = Movies.query.get(id)
            if movie:
                payload = request.get_json()
                movie.title = payload["title"]
                movie.genre = payload["genre"]
                movie.release_year = payload["release_year"]
                db.session.commit()
                return jsonify(movie.to_dict)
            else:
                return {"message": "The movie you are trying to update is not found", "type": "error"}, 404
        except Exception as e:
            db.session.rollback()
            api.abort(500, f"Internal Server Error: {str(e)}")

    @api.response(404, 'Movie not Found')
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def delete(self, id):
        ''' Delete a movie'''
        try:
            movie_to_be_deleted = Movies.query.get(id)
            if movie_to_be_deleted:
                db.session.delete(movie_to_be_deleted)
                db.session.commit()
                return f'movie with id {id} has been deleted Successfully', 200
            else:
                return {"message": "The movie you are trying to delete is not found", "type": "error"}, 404
        except Exception as e:
            api.abort(500, f"Internal Server Error: {str(e)}")

    @api.response(500, 'Internal Server Error')
    @api.response(200, 'Success')
    def get(self):
        ''' Get all movies '''
        try:
            movies = Movies.query.all()
            movies = [movie.to_dict for movie in movies]
            return jsonify({"count": len(movies), "movies": movies})
        except Exception as e:
            api.abort(500, f"Internal Server Error: {str(e)}")
