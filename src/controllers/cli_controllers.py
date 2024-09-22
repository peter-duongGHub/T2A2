from models.player import Players
from models.user import Users
from models.comments import Comments
from models.category import Category
from models.events import Events
from models.game import Games

from flask import Blueprint
from init import db, ma

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Created tables: complete")

# @db_command.cli.command("seed")
# def seed_tables():

#     user = [Player(

#     )
#     Player(

#     )
#     ]




@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Dropped tables: complete")
