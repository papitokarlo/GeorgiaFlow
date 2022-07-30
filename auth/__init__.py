from view import app, db, migrate
from flask_login import LoginManager
from flask_admin import Admin


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

admin = Admin(app)

from auth import views