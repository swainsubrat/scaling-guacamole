# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-member
# pylint: disable=cyclic-import
# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use
"""
ekart module file
"""
import os

from flask import Flask, flash, request
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdljfldldfj9743243ewjl"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ekart.db"
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024
app.config["STRIPE_PUBLIC_KEY"] = os.environ.get("STRIPE_PUBLIC_KEY")
app.config["STRIPE_PRIVATE_KEY"] = os.environ.get("STRIPE_PRIVATE_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, "static/images")
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "static/images/profiles")
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from .home.models import User  # isort:skip # noqa: E402

class MyAdminIndexView(AdminIndexView):
    """
    Class for restricting admin access
    """
    def is_accessible(self):
        """
        Method to check for accessibility
        """
        if current_user.privilage == "admin":
            return True
        return False


admin = Admin(
    app, name="Ekart Admin", template_mode="bootstrap3", index_view=MyAdminIndexView()
)

from ekart.home import routes  # isort:skip # noqa: E402

__all__ = ["User", "routes"]
