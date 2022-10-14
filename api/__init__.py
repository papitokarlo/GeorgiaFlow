from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import  os 
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

db = SQLAlchemy()

def create_app():
    templatedir = os.path.abspath('templates')
    staticdir = os.path.abspath('static')
    app = Flask(__name__, template_folder=templatedir, static_folder=staticdir)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ufp.db') #ბასა კეთდება ამ მისამართზე
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db = SQLAlchemy(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    blueprint_register(app)
    

    from auth.models import User
    from question.models import  Post, Tag
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Tag, db.session))
    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not os.path.exists("georgiaflow/api" + 'ufp.db'):
        db.create_all(app=app)
        print("Created database!")

def blueprint_register(app):
    from .views import api
    app.register_blueprint(api, url_prefix="/")
    from auth.views import auth
    app.register_blueprint(auth, url_prefix="/")
    from auth.googleauth import google_auth
    app.register_blueprint(google_auth, url_prefix="/")
    from question.views import post
    app.register_blueprint(post, url_prefix="/")