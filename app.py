import flask
import datetime
from db import db, User
from user import user

app: flask.Flask = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "NJUZ654RFVBJU765RFVBNJUZT5REW234567890POKJHVCDE34RFVJUTDU64S"
app.permanent_session_lifetime = datetime.timedelta(minutes=5)

app.register_blueprint(user)

db.init_app(app)


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

# DEBUG
@app.route("/mw/session")
def print_session():
    return flask.session

@app.route("/")
def barebone():
    return flask.redirect("/mw")

@app.route("/mw")
def home_page():

    if User.is_logged_in():
        return "User Logged In"
        # flask.render_template("index.html", username=flask.session["username"])

    flask.session["logged_in"] = False
    flask.session["username"] = None
    flask.session["role"] = 100

    return flask.redirect("/mw/user/login")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)
