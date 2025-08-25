from app import db

class KeyValue(db.Model):
    key = db.Column(db.String, primary_key=True)
    value = db.Column(db.String)