from flask import jsonify #jsonify() converts a Python dictionary into a JSON response, APIs should always return JSON instead of HTML, so jsonify is used.
from sqlalchemy.exc import SQLAlchemyError #Imports SQLAlchemy database exceptions, These occur when something goes wrong with the database.
from werkzeug.exceptions import HTTPException #Imports Flask/Werkzeug HTTP exceptions, These errors happen when route doesn't exist, wrong HTTP method used.


def register_error_handlers(app): #Defines a function that registers global error handlers for the Flask app, app is the flask application instance.
    #This is a docstring describing what the function does.
    """
    Register all global error handlers
    """

    # ---------------------------------------
    # Handle HTTP errors (404, 405, etc.)
    # ---------------------------------------
    @app.errorhandler(HTTPException) #Registers a handler for all HTTP-related errors, 404 Not Found, 405 Method Not Allowed, 403 Forbidden. Instead of Flask returning an HTML page, this function will run.
    def handle_http_exception(e): #This function executes whenever an HTTP exception occurs, e is the error object.
        return jsonify({ #Creates a JSON response.
            "error": e.name, #e.name is the name of the HTTP error.
            "message": e.description, #e.description gives a description of the error.
            "status": e.code #e.code returns the HTTP status code.
        }), e.code #Returns the JSON response with the correct status code.

    # ---------------------------------------
    # Handle database errors
    # ---------------------------------------
    @app.errorhandler(SQLAlchemyError) #Registers an error handler for database errors, These occur when SQLAlchemy fails.
    def handle_db_error(e): #Function that runs when a database error occurs, e contains the database exception.
        return jsonify({ #Creates a JSON response.
            "error": "Database Error", #Custom error name, instead of exposing internal details.
            "message": str(e) #str(e) converts the exception into readable text.
        }), 500 #Returns status code: 500=Internal Service Error

    # ---------------------------------------
    # Handle unexpected errors
    # ---------------------------------------
    @app.errorhandler(Exception) #This is a catch-all error handler, It handles any error not caught earlier.
    def handle_general_error(e): #Function executed when an unexpected error occurs.
        return jsonify({ #Returns JSON response.
            "error": "Internal Server Error", #General error message.
            "message": str(e) #Shows the actual exception message.
        }), 500 #Returns status code: 500= Internal Server Error