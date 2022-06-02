import flask
import flask_sqlalchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app: flask.Flask = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "NJUZ654RFVBJU765RFVBNJUZT5REW234567890POKJHVCDE34RFVJUTDU64S"
app.permanent_session_lifetime = datetime.timedelta(minutes=5)

db: flask_sqlalchemy.SQLAlchemy = flask_sqlalchemy.SQLAlchemy(app)

# TODO IDEA
# Have a persistent line on top of the screen,
# that changes colours depending on the login status,
# and also the role of the user
# Have a generic green for a logged in user,
# and maybe like a sexy blue for an admin
# DOES A MICROWAVE EVEN NEED AN ADMIN?
# maybe use this app as a blueprint for future projects,
# which require user access control
# /DOES A MICROWAVE EVEN NEED AN ADMIN?
# Maybe also have it display the username 
# It could be used as a redirect to the user's personal page

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(256))
    role = db.Column(db.Integer)

    def __init__(self, username: str, password: str, role=100) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    @staticmethod
    def is_username_in_use(username: str) -> bool:
        return bool(User.query.filter_by(username=username).first())

    @staticmethod
    def is_password_correct(username, heslo) -> bool:
        return check_password_hash(User.query.filter_by(username=username).first().password,heslo)

    @staticmethod
    def is_logged_in() -> bool:
        if "logged_in" in flask.session:
            if flask.session["logged_in"] == True:
                return True

        return False

    @staticmethod
    def is_admin():
        if User.is_logged_in():
            if flask.session["role"] < 100:
                return True

        return False

# @app.route("/test/<usr>")
# def testing(usr: str):
#     print(f"TYPE:{type(User.query.filter_by(username=usr).first())}")
#     print(f"BOOL:{bool(User.query.filter_by(username=usr).first())}")
#     return str(User.is_username_in_use(usr))

# TODO API/JS
# Either make two sets of apps
# One for web and another as a raw API
# Or even better, make an app and only a raw API
# What a thought

@app.route("/")
def barebone():
    return flask.redirect("/mw")

@app.route("/mw")
def home_page():

    if User.is_logged_in:
        return "User Logged In"
        # flask.render_template("index.html", username=flask.session["username"])

    flask.session["logged_in"] = False
    flask.session["username"] = None
    flask.session["role"] = 100

    return flask.redirect("/mw/user/login")

@app.route("/mw/user/new/<username>/<password>", methods=["POST","GET"])
def new_user(username: str, password: str):
    if User.is_username_in_use(username):
        return "Username is in use"
    
    db.session.add(User(username, password))
    db.session.commit()

    return "User created succesfully"

@app.route("/mw/user/login", methods=["POST","GET"])
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

@app.route("/mw/user/login/<username>/<password>", methods=["POST","GET"])
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
            password
        ):
            flask.session["logged_in"] = True
            flask.session["username"] = username
            # return flask.redirect("/mw")
            return "OK", 200

    # return flask.render_template("login.html", err=True)
    return "ERR_LOGIN", 400

@app.route("/mw/user/logout")
def logout():
    if User.is_logged_in():
        flask.session["logged_in"] = False
        flask.session["username"] = None 
        flask.session["role"] = 100

    return flask.redirect("/mw/user/login")
    # return "OK", 200

@app.route("/mw/<username>")
def test(username: str) -> str:
    return "None" if User.query.filter_by(username=username).first() == None else "Fero"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)