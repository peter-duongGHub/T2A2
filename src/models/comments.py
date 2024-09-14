from init import db, ma
from marshmallow import fields
from marshmallow.validate import And, Regexp, OneOf

class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(40), nullable=False)

    player = db.Relationship("Player", back_populates="comments")
    event = db.Relationship("Event", back_populates="comments")


class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "message", "player", "")

    message = fields.String(required=True, validate=Regexp(""), error="Invalid message format.")

comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()
