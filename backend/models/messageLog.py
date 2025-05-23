from database import db

class MessageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    role = db.Column(db.String(10))  # "user" or "agent"
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    