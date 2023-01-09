from db import db
import uuid

class MainStoreModel(db.Model):
    __tablename__ = "mainstore"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)

    tags = db.relationship("TagModel", back_populates="mainstore", lazy="dynamic")
    metastore = db.relationship("MetastoreModel", back_populates="mainstore", lazy="dynamic")
