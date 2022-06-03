import flask_sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
import flask

db: flask_sqlalchemy.SQLAlchemy = flask_sqlalchemy.SQLAlchemy()

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(256))
    role = db.Column(db.Integer)
    # TODO
    # IDEA
    # Maybe somehow log who created the user
    # Maybe if it isn't feasible with one table,
    # make a separate one for admins
    # created_by = db.relationship("User", remote_side=["_id"])

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

    @staticmethod
    def is_logged_in_admin():
        return User.is_logged_in() and User.is_admin()
