from db import db
import uuid

class MetastoreTags(db.Model):
    __tablename__ = "metastore_tags"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    metastore_id = db.Column(db.String(80), db.ForeignKey("metastore.metastore_id"))
    tag_id = db.Column(db.String(80), db.ForeignKey("tags.tag_id"))
