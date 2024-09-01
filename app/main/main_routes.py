from flask import render_template, request
from flask_login import current_user, login_required

from app.main import main_bp as main
from app.models import User


@main.route("/", endpoint="welcome")
def index():
    if not current_user.is_authenticated:
        return render_template("index.html")
    return render_template("main/login.html")


@main.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        return render_template("main/home.html")
    return render_template("main/home.html")


@main.route("/favorites", methods=["GET", "POST"])
@login_required
def table():
    pass


@main.route("/favorite/<manga_name>", methods=["GET", "POST"])
@login_required
def gate(manga_name):
    if request.method == "GET":
        return render_template("main/gates.html")
    return render_template("main/gates.html")


@main.route("/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    user = User(username).get_user()
    if user is None:
        return render_template()
