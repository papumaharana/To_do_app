from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Creating database object

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'   
    #if use mysql : Make sure "To_do_app" database already created
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2266@localhost/to_do_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.__init__(app)  # Connect to database


    # all routes connect to app:
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
