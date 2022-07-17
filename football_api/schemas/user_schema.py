from marshmallow import Schema, fields, post_load
from football_api.models import User


class UserSchema(Schema):
    """
    User Marshmallow Schema.
    """

    uuid = fields.UUID(allow_none=False)
    first_name = fields.String(allow_none=False)
    last_name = fields.String(allow_none=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
