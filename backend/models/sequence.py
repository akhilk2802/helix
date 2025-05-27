from database import db

class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    step = db.Column(db.Integer)
    content = db.Column(db.Text)
    channel = db.Column(db.String(20))
    sequence_id = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())