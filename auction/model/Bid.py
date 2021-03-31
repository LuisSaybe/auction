from tortoise.models import Model
from tortoise import fields


class Bid(Model):
    id = fields.IntField(pk=True)
    by_user = fields.IntField()
    bid_amount = fields.IntField()
    item = fields.ForeignKeyField(
        'models.Item', related_name='bids')
