from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import jwt_required
from db import db
from models import MetastoreModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Metastore", "metastore", description="Operations on metastore")


@blp.route("/metastore/<string:metastore_id>")
class Metastore(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, metastore_id):
        metastore = MetastoreModel.query.get_or_404(metastore_id)
        return metastore

    def delete(self, metastore_id):
        item = MetastoreModel.query.get_or_404(metastore_id)
        db.session.delete(metastore_id)
        db.session.commit()
        return {"message": "Metastore deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, metastore_data, metastore_id):
        metastore = MetastoreModel.query.get(metastore_id)

        if metastore:
            #metastore.source = metastore_data["source"]
            metastore.name = metastore_data["name"]
        else:
            metastore = MetastoreModel(id=metastore_id, **metastore_data)

        db.session.add(metastore)
        db.session.commit()

        return metastore


@blp.route("/metastore")
class MetastoreList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return MetastoreModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, metastore_data):
        metastore = MetastoreModel(**metastore_data)

        try:
            db.session.add(metastore)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return metastore
