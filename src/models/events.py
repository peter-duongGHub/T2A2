# from init import db, ma
# from marshmallow import fields
# from marshmallow.validate import And, Regexp, OneOf

# class Event(db.Model):
#     __tablename__ = "events"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(40), nullable=False)
#     description = db.Column(db.String(40), nullable=True)
#     date = db.Column(db.Date)
#     duration = db.Column(db.Integer, primary_key=True)

#     player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)

#     user = db.Relationship("User", back_populates="event")
#     comments = db.Relationship("Comment", back_populates="event")


# class EventSchema(ma.Schema):


#     class Meta:
#         fields = ("id", "name", "description", "date", "duration")

#     name = fields.String(required=True, validate=Regexp(""))
#     description = fields.String(required=True, validate=Regexp(""))
#     duration = fields.String(required=True, validate=Regexp(""))

# events_schema = EventSchema(many=True)
# event_schema = EventSchema()