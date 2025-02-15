import uuid
from datetime import datetime
from config import db

# pylint: disable=W0611
from utils.base_models import ETBaseMixin
from ..bid.model import Bid

# pylint: disable=W0611


class BidSubmit(db.Model, ETBaseMixin):
    __tablename__ = 'bidsubmit'
    uuid = db.Column(db.String(40), primary_key=True, unique=True, nullable=False)
    bid_type = db.Column(db.String(40))  # sell or buy
    time = db.Column(db.DateTime, unique=False, nullable=False)
    value = db.Column(db.Float)
    price = db.Column(db.Float)
    upload_time = db.Column(db.Date, unique=False, nullable=False)
    # ForeignKey to Bid
    bid_id = db.Column(db.String(80), db.ForeignKey('bid.uuid'), nullable=False)
    bid = db.relationship(Bid)

    def __init__(self, bid_type, time, value, price, bid_id):
        self.uuid = str(uuid.uuid4())
        self.bid_type = bid_type
        self.time = time
        self.value = value
        self.price = price
        self.upload_time = datetime.today()
        self.bid_id = bid_id
