from models.player import Player
# from models.comments import Comments
# from models.category import Category
# from models.events import Event
# from models.game import Game
# from models.progress import Progress

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
