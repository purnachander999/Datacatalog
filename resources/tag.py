from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import jwt_required
from db import db
from models import TagModel, MainStoreModel, MetastoreModel
from schemas import TagSchema, TagAndItemSchema,TagUpdateSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/mainstore/<string:mainstore_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, mainstore_id):
        store = MainStoreModel.query.get_or_404(mainstore_id)

        return store.tags.all()  # lazy="dynamic" means 'tags' is a query



    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, mainstore_id):
        # if TagModel.query.filter(TagModel.mainstore_id == mainstore_id).first():
        #     abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, mainstore_id=mainstore_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )
        return tag

@blp.route("/tag/<string:tag_id>")
class TagList(MethodView):

    @blp.arguments(TagUpdateSchema)
    @blp.response(200, TagSchema)
    def put(self, tag_data, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag:
            tag.name = tag_data["name"]
        else:
            tag = MetastoreModel(id=tag_id, **tag_data)

        db.session.add(tag)
        db.session.commit()
        return tag


@blp.route("/metastore/<string:metastore_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, metastore_id, tag_id):
        metastore = MetastoreModel.query.get_or_404(metastore_id)
        tag = TagModel.query.get_or_404(tag_id)

        metastore.tags.append(tag)

        try:
            db.session.add(metastore)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, metastore_id, tag_id):
        metastore = MetastoreModel.query.get_or_404(metastore_id)
        tag = TagModel.query.get_or_404(tag_id)

        metastore.tags.remove(tag)

        try:
            db.session.add(metastore)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tag")
class Get_all_tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag




    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa: E501
        )
