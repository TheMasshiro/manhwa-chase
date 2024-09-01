import logging

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth_bp as auth
from app.forms import LoginForm, RegisterForm
from app.helpers import recaptcha_key, verify_user
from app.models import User


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout User"""
    logout_user()
    return redirect(url_for("main.welcome"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in user
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data).get_user()

        if user is None or not user.check_password(form.password.data):
            return redirect(url_for("auth.login"))

        try:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("main.home"))
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")

    return render_template("auth/login.html", title="Log in", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    Register user
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()
    if form.validate_on_submit():
        verify_user()

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        is_created = user.create_user()

        if not is_created:
            flash("An error has occurred")
            return redirect(url_for("auth.register"))

        try:
            login_user(user.get_user(), remember=form.remember_me.data)
            return redirect(url_for("main.home"))
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")

    return render_template(
        "auth/register.html", title="Register", form=form, site_key=recaptcha_key()
    )
