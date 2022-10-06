#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_cors import CORS
from flask import (
    Flask, 
    redirect, 
    abort, 
    jsonify,
    request
)
import collections
import collections.abc
collections.Callabsle = collections.abc.Callable
from models import (
    Book,
    Genre,
    app, 
    db, 
)
from auth import AuthError, requires_auth, API_AUDIENCE, AUTH0_DOMAIN
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

CLIENT_ID = '5tKdYhNmdKPdR03AYsXWwEuJIQo7TFxo'

def create_app(test_config=None):

    CORS(app, resources={r"/*": {"origins": "*"}})
 
    # CORS Headers - Setting access control allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
 
    @app.route('/')
    def get_greeting():
        return "Hi, Welcome"

    # login endpoint which will redirect you to the auth0 sign in page
    @app.route('/login')
    def login():
        return redirect('https://' + AUTH0_DOMAIN + '/authorize?audience=' + API_AUDIENCE +'&response_type=token&client_id=' + CLIENT_ID + '&redirect_uri=' + request.host_url)

    # logout endpoint which will redirect you to the auth0 logout page
    @app.route('/logout')
    def logout():
        return redirect('https://' + AUTH0_DOMAIN + '/v2/logout?audience=' + API_AUDIENCE + '&client_id=' + CLIENT_ID + '&returnTo=' + request.host_url + 'logout-results')

    # endpoint needs a user with get:genres permission to fetch all the genres 
    @app.route('/genres')
    @requires_auth('get:genres')
    def retrieve_genres(payload):
        """ Endpoint to handle GET requests for all questions paginated (10 questions) """
        try:
            genres = Genre.query.all()
        except Exception as e:
            print(e)
            abort(422)
        
        formatted_genres = [genre.format() for genre in genres]

        return jsonify({
            'success': True,
            'Genre': formatted_genres,
            'total_Genres': len(formatted_genres)
        })


    # endpoint which needs a user with delete:genres permission to delete a genre with id = id
    @app.route('/genres/<int:id>', methods=['DELETE'])
    @requires_auth('delete:genres')
    def delete_genre(payload,id):
        try:
            genre = Genre.query.filter_by(id=id).one_or_none()
        except:
            abort(422)
        if genre is None:
            abort(404)
        try:
            genre.delete()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'deleted': id
        })

    # endpoint which needs a user with post:genres permission to post a new genre in the db
    @app.route('/genres', methods=['POST'])
    @requires_auth('post:genres')
    def create_genres(payload):
        """ Endpoint to POST a new question """
        body = request.get_json()

        # Check that we are getting the required fields
        if not ('name' in body):
            abort(422)

        new_name = body.get('name', None)

        try:
            genre = Genre(name=new_name)
            genre.insert()
            return jsonify({
                'success': True,
                'created': genre.id,
            })
        except:
            abort(422)     

    # API endpoint to fetch all books from db 
    # Only user with get:books permission can access it 
    @app.route('/books')
    @requires_auth('get:books')
    def retrieve_books(payload):
        try:
            print(111)
            books = Book.query.all()
            print(111)
        except:
            abort(422)
        
        formatted_books = [book.format() for book in books]
        if not formatted_books:
             abort(404)

        return jsonify({
            'success': True,
            'bookings': formatted_books,
            'total_bookings': len(formatted_books)
        })

    # API endpoint to fetch a book's detail from db with id = id
    # Only user with get:books-details permission can access it 
    @app.route('/books/<int:id>')
    @requires_auth('get:books-details')
    def retrieve_book(payload,id):

        book = Book.query.filter_by(id=id).one_or_none()
        if book is None:
            print('404')
            abort(422)
        
        # Make sure it found a booking
        if book is None:
             abort(404)

        return jsonify({
            'success': True,
            'id': book.id,
            'book_name': book.book_name,
            'Genre_id': book.Genre_id,
            'book_description': book.book_description
        })

    # API endpoint to posts a new book detail to db
    # Only user with post:books permission can access it 
    @app.route('/books', methods=['POST'])
    @requires_auth('post:books')
    def create_booking(payload):
        """ Endpoint to POST a new booking """
        body = request.get_json()

        id = body.get('book_id', None)
        name = body.get('book_name', None)
        book_description = body.get('book_description', None)
        Genre_name = body.get('Genre_name', None)
        
        genre = Genre.query.filter_by(name=Genre_name).one_or_none()
        if genre is None:
            genre_add = Genre(name = Genre_name)
            genre_add.insert()
        genre = Genre.query.filter_by(name=Genre_name).one_or_none()

        book = Book(id=id, book_name=name, book_description=book_description, Genre_id= genre.id)
        try:
            book.insert()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'created': book.id,
        })


    #Error handlers for all expected errors 

    @app.errorhandler(400)
    def error_bad_request(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def error_unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity"
        }), 422
        
    @app.errorhandler(405)
    def error_methodNotAllowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()