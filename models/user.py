from db import db
import uuid

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

