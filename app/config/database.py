import os #os is a Python bulit-in-module, it allows us to interact with the operating system
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy is an ORM, which lets us work with databses using Python classes instead of SQL queries

db = SQLAlchemy() #creates an instance of SQLAlchemy & db will be used throughout the project to define database models, create tables, query data, insert/update/delete records

#This defines a function called init_db, It takes app as a parameter, app is the Flask application instance
def init_db(app): 
    #This sets the database connection string, Flask stores configuration settings in app.config, "SQLALCHEMY_DATABASE_URI" This tells SQLAlchemy which database to connect to.
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///app.db" #create/use app.db file in project folder
    ) #This reads an environment variable.
    #Use DATABASE_URL if it exists; otherwise use the SQLite database app.db.

    #This disables extra overhead tracking to save memory, improve performance, remove warning messages.
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #This connects the SQLAlchemy instance (db) to the Flask app. Without this, the database will not work with Flask.
    db.init_app(app)


def create_tables(app): #This function creates database tables, also receives the Flask app instance.
    with app.app_context(): #This line temporarily activates the Flask app environment.
        db.create_all() #Reads all models defined using db.Model, Creates corresponding tables in the database