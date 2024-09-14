from init import db, ma
from marshmallow.validate import fields

class Progress(db.Model):
    __tablename__ = "progress"
    id = db.Column(db.Integer, primary_key=True)
    progress = db.Column(db.Integer)
    date = db.Column(db.Date)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    events_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    player = db.Relationship("Progress", back_populates="progresses")
    event = db.Relationship("Event", back_populates="progress")

class ProgressSchema(ma.Schema):

    log = fields.Nested("LogSchema",)
    event = fields.Nested("EventSchema",)

    class Meta:
        fields = ("id", "progress", "date", "log", "event")




progresses_schema = ProgressSchema(many=True)
progress_schema = ProgressSchema()