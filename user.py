from flask.blueprints import Blueprint
import flask
from db import db, User

user = Blueprint(
    "user",
    __name__, 
    static_folder="static", 
    template_folder="templates",
    url_prefix="/mw/user"
)

@user.route("/new/<username>/<password>/<role>", methods=["POST","GET"])
def new_user(username: str, password: str, role=100):
    if User.is_username_in_use(username):
        return "Username is in use"
    
    db.session.add(User(username, password, role))
    db.session.commit()

    return "User created succesfully"

@user.route("/login", methods=["POST","GET"])
def login():
    if "logged_in" in flask.session and flask.session["logged_in"] == True:
        return "OK", 200

    if flask.request.method == "GET":
        return flask.render_template("login.html")

    # TODO JS
    # make the front end only send in requests
    # with valid usernames
    # make an edpoint, that solely checks for username existance
    # SECURITY
    # limit the rate at which the username existance can be requested

    if User.is_username_in_use(flask.request.form["user"]):
        if User.is_password_correct(
            flask.request.form["user"],
            flask.request.form["pass"]
        ):
            flask.session["logged_in"] = True
            flask.session["username"] = flask.request.form["user"]
            return flask.redirect("/mw")
            # return "OK", 200

    return flask.render_template("login.html", err=True)
    # return "ERR_LOGIN", 400

@user.route("/login/<username>/<password>", methods=["POST","GET"])
def login_API(username, password):
    if User.is_logged_in():
        return "OK", 200

    # if flask.request.method == "GET":
    #     return flask.render_template("login.html")

    # TODO JS
    # make the front end only send in requests
    # with valid usernames
    # make an edpoint, that solely checks for username existance
    # SECURITY
    # limit the rate at which the username existance can be requested

    if User.is_username_in_use(username):
        if User.is_password_correct(
            username,
            password,
        ):
            flask.session["logged_in"] = True
            flask.session["username"] = username
            flask.session["role"] = User.query.filter_by(username=username).first().role
            # return flask.redirect("/mw")
            return "OK", 200

    # return flask.render_template("login.html", err=True)
    return "ERR_LOGIN", 400

@user.route("/logout")
def logout():
    if User.is_logged_in():
        flask.session["logged_in"] = False
        flask.session["username"] = None 
        flask.session["role"] = 100

    return flask.redirect("/mw/user/login")
    # return "OK", 200

@user.route("/<username>")
def test(username: str) -> str:
    return "None" if User.query.filter_by(username=username).first() == None else "Fero"
