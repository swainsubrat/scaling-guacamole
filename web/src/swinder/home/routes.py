# pylint: disable=no-member
"""
Routes file for home
"""
import os

from swinder import app, bcrypt, db
from swinder.utils.constants import ACTIONS, REGISTERED_IDS
from swinder.utils.aws_utils import publish
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

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
    return render_template("home/home1.html", title="Home")


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


@app.route("/operation")
def operation():
    """
    1. Get the id
    2. AWS IoT -> On the window with id : id
    3. Get response
    4. Return response
    """
    response = {"isSuccess": False}
    id       = request.args.get("id")
    action   = request.args.get("action")
    angle    = request.args.get("angle", 90)

    if id not in REGISTERED_IDS:
        response["message"] = "Requested device is not registered!!!"
        return response

    if action not in ACTIONS:
        response["message"] = f"Requested Action doesn't exist, Try among {ACTIONS}!!!"
        return response
    
    message = {}
    message["id"] = id
    message["action"] = action
    message["angle"]  = angle

    is_success = publish(message=message, topic="user_publish")

    if is_success:
        response["isSuccess"] = is_success
    else:
        response["message"] = is_success

    return response

@app.route("/window1", methods=["GET", "POST"])
def window1():
    return render_template("home/window1.html", title="window1")

@app.route("/window2", methods=["GET", "POST"])
def window2():
    return render_template("home/window2.html", title="window2")

@app.route("/window3", methods=["GET", "POST"])
def window3():
    return render_template("home/window3.html", title="window3")

@app.route("/window4", methods=["GET", "POST"])
def window4():
    return render_template("home/window4.html", title="window4")

@app.route("/window5", methods=["GET", "POST"])
def window5():
    return render_template("home/window5.html", title="window5")

@app.route("/window6", methods=["GET", "POST"])
def window6():
    return render_template("home/window6.html", title="window6")