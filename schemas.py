from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    headers = fields.Dict(keys=fields.Str(), values=fields.Str(), required=False)
    trans_comments = fields.Str(required=True)
    source = fields.Str(required=True)
    timestamp = fields.DateTime()



class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    description = fields.Str()


class PlainTagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    mainstore_id = fields.Str(required=True, load_only=True)
    mainstore = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    metastore = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    mainstore_id = fields.Str(dump_only=True)
    metastore = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    mainstore = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    metastore = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
