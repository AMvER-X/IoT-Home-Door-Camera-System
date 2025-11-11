from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Creating database
class Capture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Look into fixing
    data = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(150))
    captures = db.relationship('Capture')