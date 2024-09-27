# Imported models for creating tables and seeding values for testing 
from models.player import Players
from models.user import Users
from models.comments import Comments
from models.events import Events
from models.game import Games

# Import Blueprint to use decorate routes from main.py file
from flask import Blueprint
# Import initialised SQLAlchemy and Bcrypt object instances
from init import db, bcrypt

db_commands = Blueprint("db", __name__)

# Creating table entities based on imported models 
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Created tables: complete")

# Seeding created values into the tables for testing purposes
@db_commands.cli.command("seed")
def seed_tables():

    users = [Users(
        username = "random",
        password = bcrypt.generate_password_hash("1234").decode("utf-8"),
        email = "random@gmail.com",
        is_authorised = True
    ),
    Users(
        username = "Peter",
        password = bcrypt.generate_password_hash("444").decode("utf-8"),
        email = "peter@gmail.com"
    )
    ]

    # Adding seeded values for user objects to database session 
    db.session.add_all(users)

    games = [Games(
        name = "CallOfDuty",
        description = "Shooter",
        user = users[1]
    ),
    Games(
        name = "League",
        description = "RPG",
        user = users[1]
    ),
    Games(
        name = "Minecraft",
        description = "Building",
        user = users[1]
    )
    ]

    # Adding seeded values for games objects to database session 
    db.session.add_all(games)

    players = [Players(
        name = "Peter",
        date = "2024/05/05",
        role = "Tank",
        game = games[0],
        user = users[1]

    ),
    Players(
        name = "Random",
        date = "2025/06/06",
        role = "DPS",
        game = games[0],
        user = users[0]


    ),
    Players(
        name = "Open",
        date = "2026/02/02",
        role = "Healer",
        game = games[0],
        user = users[1]
    )
    
    ]

    # Adding seeded values for players objects to database session 
    db.session.add_all(players)

    events = [
        Events(
        description = "ACTION",
        date = "2025/05/05",
        duration = 15,
        player = players[0]
    ),

    Events(
        description = "QUEST",
        date = "2024/02/02",
        duration = 10,
        player = players[0]

    ),

    Events(
        description = "SOCIAL",
        date = "2021/02/02",
        duration = 2,
        player = players[0]
    )
    ]

    # Adding seeded values for events objects to database session 
    db.session.add_all(events)

    comments = [
        
        Comments(
          message = "Finished slaying dragon",
          event = events[0],
          player = players[0]  
        ),
        Comments(
            message = "Talked to friends today",
            event = events[2],
            player = players[0]
        ),
        Comments(
            message = "Handed in quest",
            event = events[1],
            player = players[0]
        )
    ]

    # Adding seeded values for comments objects to database session 
    # Commit all added objects to the database session
    # Print statement to confirm seeding of tables
    db.session.add_all(comments)
    db.session.commit()
    print("Tables seeded.")

# Cli command to drop all tables if needed or when finished 
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Dropped tables: complete")
