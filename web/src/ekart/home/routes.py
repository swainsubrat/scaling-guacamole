# pylint: disable=no-member
"""
Routes file for home
"""
import os

from ekart import app, bcrypt, db
# from ekart.products.models import Products
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
# from minio import Minio

# from werkzeug.utils import secure_filename
from .forms import LoginForm, RegistrationForm
from .models import User


@app.errorhandler(404)
def page_not_found(error_code):
    """
    404 Page
    """
    if error_code != 404:
        error_code = 404
    return render_template("admin/page_404.html"), error_code

@login_required
@app.route("/home")
def home():
    """
    Endpoint for home
    """
    # page = request.args.get("page", 1, type=int)
    # products = Products.query.filter(Products.price > 0)
    # pages = products.paginate(page=page, per_page=8)
    return render_template(
         "home/home1.html", title="Home"
    )
    return "This is home page"


@app.route("/")
@app.route("/landing")
def landing_page():
    """
    Endpoint for landing page
    """
    return render_template("home/landing_page.html", title="Homepage")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Endpoint for register
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("home/register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Endpoint for login
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()

    # if valid submission(after checks)
    if form.validate_on_submit():

        # find the user from the db
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # login the user and remember the user according to the remember me value.
            login_user(user, remember=form.remember.data)

            # if user is trying to access some page, after login, he should be
            # directed to that path, not home page.
            # next_page = request.args.get("next")
            # return redirect(next_page) if next_page else redirect(url_for("home"))
            return redirect(url_for("home"))

        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("home/login.html", title="Login", form=form)


@login_required
@app.route("/logout")
def logout():
    """
    Endpoint for logout
    """
    logout_user()
    return redirect(url_for("home"))

@app.route("/window1", methods=["GET", "POST"])
def window1():
    return render_template("home/window1.html", title="window1")






# @login_required
# @app.route("/window1")
# def window1():
#     """set up for window1"""
#     return redirect(url_for("window1.html"))
# @login_required
# @app.route("/profile", methods=["GET", "POST"])
# def profile():
#     """
#     Endpoint to show profile page
#     """
#     path = os.path.join(app.config["UPLOAD_FOLDER"], f"{current_user.username}_img.jpg")
#     allowed_file_types = ["jpg", "jpeg", "png"]

#     # Connect to minio
#     minio_client = Minio(
#         "minio:9000",
#         access_key=os.environ.get("MINIO_ACCESS_KEY"),
#         secret_key=os.environ.get("MINIO_SECRET_KEY"),
#         secure=False,
#     )

#     # Check for bucket named current_user.username
#     found = minio_client.bucket_exists(current_user.username)

#     # if present, fetch image and return
#     if found:
#         minio_client.fget_object(
#             current_user.username, f"{current_user.username}_img.jpg", path
#         )

#     if request.method == "POST":
#         if request.files["image"].filename != "":
#             image = request.files["image"]
#             extension = image.split(".")[1]
#             if extension in allowed_file_types:
#                 image.save(path)

#                 # Check for bucket name, if not present create and upload
#                 if not found:
#                     minio_client.make_bucket(current_user.username)
#                 minio_client.fput_object(
#                     current_user.username, f"{current_user.username}_img.jpg", path
#                 )

#                 return render_template(
#                     "home/profile.html",
#                     title="Profile",
#                     present=True,
#                     filename=f"{current_user.username}_img.jpg",
#                 )
#             else:
#                 flash("Wrong file format, please upload again", "warning")
#     return render_template(
#         "home/profile.html",
#         title="Profile",
#         present=found,
#         filename=f"{current_user.username}_img.jpg",
#     )
