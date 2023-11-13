from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = '8d9a018d01741fc317ce5e4050ee3740' #generated using secret module
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #/// is for the relative paths, means that site.db will be created in the same file where py file is there
db = SQLAlchemy(app) #instance of sqlalchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskBlog import routes

app.app_context().push()