from db import db
import uuid

class MainStoreModel(db.Model):
    __tablename__ = "mainstore"

    mainstore_id = db.Column(db.String(220), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(220), unique=True, nullable=False)

    tags = db.relationship("TagModel", back_populates="mainstore", lazy="dynamic")
    metastore = db.relationship("MetastoreModel", back_populates="mainstore", lazy="dynamic")
