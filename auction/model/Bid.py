from tortoise.models import Model
from tortoise import fields


class Bid(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    amount = fields.IntField()
    item = fields.ForeignKeyField(
        'models.Item', related_name='bids')
