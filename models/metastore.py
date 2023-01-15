from db import db
import uuid
from datetime import datetime


class MetastoreModel(db.Model):
    __tablename__ = "metastore"

    metastore_id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=False, nullable=False)
    field_names = db.Column(db.JSON, nullable=False)
    trans_comments = db.Column(db.String(80), unique=False, nullable=False)
    source = db.Column(db.String(80), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



    mainstore_id = db.Column(
        db.String(80), db.ForeignKey("mainstore.mainstore_id"), unique=False, nullable=False
    )
    mainstore = db.relationship("MainStoreModel", back_populates="metastore")

    tags = db.relationship("TagModel", back_populates="metastore", secondary="metastore_tags")
