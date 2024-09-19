from init import db, ma
from marshmallow import fields

class Records(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    progress = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    # player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    # events_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    # player = db.Relationship("Record", back_populates="records")
    # event = db.Relationship("Event", back_populates="records")

class RecordSchema(ma.Schema):

    # log = fields.Nested("LogSchema",)
    # event = fields.Nested("EventSchema",)

    class Meta:
        fields = ("id", "progress", "date")




records_schema = RecordSchema(many=True)
record_schema = RecordSchema()