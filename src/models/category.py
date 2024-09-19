from init import db, ma
from marshmallow import fields

# DESCRIPTION = ("CHARACTER", "ACTION", "SOCIAL")

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    event = db.Relationship("Events", back_populates="categories")

class CategorySchema(ma.Schema):

    event = fields.Nested("EventSchema", exclude=["categories"])

    class Meta:
        fields = ("id", "name", "description", "event")

categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()