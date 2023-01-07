from db import db
import uuid
from datetime import datetime


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    header = db.Column(db.JSON, nullable=False)
    comments = db.Column(db.String(80), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



    store_id = db.Column(
        db.String(80), db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")

    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
