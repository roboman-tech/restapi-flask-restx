from flask_restx import Api, Resource, fields
from api import app
api = Api(app)

movie_model = api.model(
    'Movies',
     {
         'title': fields.String(),
         'genre': fields.String(),
         'release_year': fields.Integer()
     }
 )