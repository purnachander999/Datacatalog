from db import db
import uuid

class TagModel(db.Model):
    __tablename__ = "tags"

    tag_id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    mainstore_id = db.Column(db.String(80), db.ForeignKey("mainstore.mainstore_id"), nullable=False)

    mainstore = db.relationship("MainStoreModel", back_populates="tags")
    metastore = db.relationship("MetastoreModel", back_populates="tags", secondary="metastore_tags")
