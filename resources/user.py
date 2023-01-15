from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token

from db import db
from models import TagModel, MainStoreModel, MetastoreModel, UserModel
from schemas import TagSchema, TagAndItemSchema, UserSchema, UserUpdateSchema


blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        print("*******************")
        print(UserModel.username)
        print("********************")
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, "A username with the username already exists")

        user = UserModel(
            username = user_data["username"],
            password = user_data["password"]
        )

        db.session.add(user)
        db.session.commit()

        return user

@blp.route("/login")
class UserLogin(MethodView):

    @blp.response(200, UserSchema(many=True))
    def get(self):
        print("I am in get")
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and (user_data["password"] == user.password):
            print("verified")
            access_token = create_access_token(identity=user.user_id)
            return {"access_token": access_token}
        abort( 401, message="invalid credentails")


@blp.route("/user/<string:user_id>")
class User(MethodView):
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get(user_id)

        if user:
            user.password = user_data["password"]
        else:
            user = MetastoreModel(id=user_id, **user_data)

        db.session.add(user)
        db.session.commit()

        return user


    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"user deleted"}, 200