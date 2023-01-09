import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import MainStoreModel
from schemas import StoreSchema


blp = Blueprint("Mainstore", "mainstore", description="Operations on Mainstore")


@blp.route("/store/<string:mainstore_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, mainstore_id):
        store = MainStoreModel.query.get_or_404(mainstore_id)
        return store

    def delete(self, mainstore_id):
        store = MainStoreModel.query.get_or_404(mainstore_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return MainStoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = MainStoreModel(**store_data)
        print(store)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name  chandu already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store
