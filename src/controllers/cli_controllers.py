from models.player import Player
from models.comments import Comments
from models.category import Category
from models.events import Event
from models.game import Game
from models.progress import Progress

from flask import Blueprint
from init import db, ma

cli_bp = Blueprint("cli", __name__)

@cli_bp.cli.command("create")
def create_tables():
    db.create_all()
    print("Created tables: complete")


