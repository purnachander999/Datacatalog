from db import db
import uuid

class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    item_id = db.Column(db.String(80), db.ForeignKey("items.id"))
    tag_id = db.Column(db.String(80), db.ForeignKey("tags.id"))
