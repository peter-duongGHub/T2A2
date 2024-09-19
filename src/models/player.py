# from init import db, ma
# from marshmallow import fields

# class Player(db.Model):
#     __tablename__ = "player"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     level = db.Column(db.Integer, default=0)
#     date = db.Column(db.Date, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     email = db.Column(db.String, unique=True)
#     is_authorised = db.Column(db.Boolean, default=False)
    
#     # game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

#     # game = db.Relationship("Games", back_populates="players")
#     # comments = db.Relationship("Comments", back_populates="player")
#     # progresses = db.Relationship("Progress", back_populates="player")

# class PlayerSchema(ma.Schema):

#     game = fields.Nested("GameSchema", only=["name", "description", "user"])
#     # comments = fields.Nested("CommentSchema", only=["id", "message"])
#     # progresses = fields.Nested("ProgressSchema", only=["progress, date"])


#     class Meta:
#         fields = ("id", "name", "level", "date", "password", "email", "is_authorised")

# players_schema = PlayerSchema(exclude=["password"], many=True)
# player_schema = PlayerSchema(exclude=["password"])
