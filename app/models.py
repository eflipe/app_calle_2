from app import db
from datetime import datetime


class AppData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_geo = db.Column(db.String(345), index=True, unique=False)
    street_search = db.Column(db.String(345), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<ID: {self.id}, GEO: {self.street_geo}, SEARCH: {self.street_search}, TIME: {self.timestamp}>'
