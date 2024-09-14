from init import db, ma
# from marshmallow import fields

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), unique=True)

    # comments = db.Relationship("Comments", back_populates="player")
    # progresses = db.Relationship("Progress", back_populates="player")

class PlayerSchema(ma.Schema):

    # comments = fields.Nested("CommentSchema", only=["id", "message"])
    # progresses = fields.Nested("ProgressSchema", only=["progress, date"])


    class Meta:
        fields = ("id", "level", "date", "password", "email")

players_schema = PlayerSchema(exclude=["password"], many=True)
player_schema = PlayerSchema(exclude=["password"])
