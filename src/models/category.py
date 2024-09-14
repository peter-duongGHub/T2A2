from init import db, ma

DESCRIPTION = ("CHARACTER", "ACTION", "SOCIAL")

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(40), nullable=False)

    events = db.Relationship("Event", back_populates="category")

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description")

categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()