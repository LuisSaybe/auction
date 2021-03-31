from tortoise.models import Model
from tortoise import fields


class Item(Model):
    id = fields.IntField(pk=True)
    auction_end_date = fields.DatetimeField()
