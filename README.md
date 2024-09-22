# T2A2 API WebServer - Game Event Tracker

Table of Contents
## R1 - Explain the problem you are trying to solve and how the app solves the problem
## R2 - Task Management - Trello and Github
## R3 - Third-Party Services, Packages & Dependencies
## R4 - Benefits and drawbacks of PostgreSQL
## R5 - Explain features, purpose and functionalities of ORM in the app
## R6 - An ERD for your app
## R7 - Explain models and their relationships and explain how relationships aid database implementation
## User Model
## Game Model
## Player Model
## Comments Model
## Records Model
## Events Model
## Category Model
## R8 - Explain app's API endpoints including:
- HTTP verb
- Path or route
- Any required body or header data
- Response


## R1
### Explain Solved Problem
With the increasing popularity of games, the management and analysis of past in-game events becomes increasingly more significant as the player base and complexities of games evolve. A common denominator within most games is the absence of in-game event tracking whereby players have a way to execute events but they do not have a way to review each past event committed. Having an event tracker can help players review any changes to their characters and track the progressive development of characters on an ongoing basis, this can help prevents users from spending far too much time on the game if they have progressed a certain amount and for users that are forgetful, they're able to account for what they previously did with their players. 

### Explain How problem is addressed and References
This app works by using




## R2 Task allocation and Management - Trello & GitHub
### Trello
For this application Trello was used for management of tasks and acted as a sort of checklist to ensure all rubric was covered and completed as well as the flow of creating the application was consistent and gradual. Specific dates were allocated to each task and objective to ensure the application was progressing according to plan towards the submission date. Trello was used for organisation of the project, time management and tracking tasks as well as visualises the workflow. Each card used a colour coded system for categorisation of tasks and different cards were allocated to define milestones and deadlines. Checklists within each card were to help break down components of each card further and to emphasise points required for the rubric of the T2A2 Webserver assignment.

![https://trello.com/b/9sVow73W/t2a2-api-webserver]()

#### Reference
![Trello-Image]()


### GitHub
Github was used to track changes and recovery of data if necessary. Throughout the length of the project each file that had been completed had a git operation performed to push the local repository changes to a remote repository (github) to help with debugging, organisation and collaboration (where necessary). GitHub was also used as a requirement for this assignment T2A2 to help track changes to the project.

#### Example of how this was done
1. Login to Github and create a new repository
2. Create new local directory on computer
3. Open Ubuntu
4. Initialise local repository with: ```git init```
5. Echo a read me file: ```echo "T2A2" >> README.md```
6. Add any changes to a staging area for the current directory: ```git add .```
7. Commit changes in staging area with a meaningful message: ```git commit -m "first commit"```
8. Ensure the current branch is main: ```git branch -M main```
9. Add origin of remote repository: ```git remote add origin git@github.com:peter-duongGHub/T2A2-1.git```
10. Push upstream to the main branch as origin: ```git push -u origin main```

![GitHub-Project]()

#### Reference
![GitHub-Image]()


## R3
### Dependencies 
An extensive explanation of each dependency used in this application can be found below:
> Prior to installation of each package users should work in a virtual environment to prevent conflictions with other project dependency versions:

### Installation:
#### Virtual Environment
Virtual environment is used to keep my dependencies contained for this specific project to reduce contingencies and overlap with other projects users might be involved with - maintaining module versions and preventing overlapping of dependency versions.

1. Setup virtual environment

```python3 -m venv venv```

2. Activate the virtual environment

``` source venv/bin/activate```

#### Psycopg2
Psycopg2 is a popular PostgreSQL adapter for Python that provides a robust interface for connecting to and interacting with PostgreSQL databases. It’s designed to be efficient, secure, and easy to use, making it one of the most widely used libraries for PostgreSQL database management in Python applications such as my game event tracker application. It acts as a mediator between my application logic and PostgreSQL ensuring operations and requests to the database function smoothly. 

##### Installation
1. Install psycopg2 package

``` pip install psycopg2-binary```

##### Description

#### Python Dotenv
Python dotenv is used in this application to help with configuration setttings stored within an .env file. This helps with modularisation as it seperates the application logic from the configuration data. It is utilised to help with configuring the jwt secret key, database URL, database adapter, user and password. For the example below the ```os``` module is imported and used with ```os.environ.get("variable")``` to link the configuration settings to the .env file where ```("variable")``` would be replaced with the configuration setting variable such as ```SECRET_KEY``` in the .env.example file.

Example:

![Python-Dotenv](./docs/env.PNG)


![Python-Dotenv](./docs/env2.PNG)


##### Installation
1. Install python-dotenv package

``` pip install python-dotenv```


#### PostgreSQL
PostgreSQL is the database system that my application will be using. The purpose of PostgreSQL is to act as an relational database management system (RDBMS) by storing data within tables that consist of rows and columns. Specifically for this application, PostgreSQL is used to help store user input into a relational database. This is greatly beneficial for users who use my API webserver as they can store data and retrieve that stored data whenever necessary.
It contains many components and features that are used within this application such as constraints including:
- Primary Keys
- Foreign Keys
- Unique Constraints
- Default Constraints
- Nullable Constraints

#### Flask
Flask is a lightweight web framework for Python that allows developers to build web applications quickly and easily. Flask depends on the Werkzeug WSGI toolkit, the Jinja template engine, and the Click CLI toolkit. It does have many cool features like url routing, template engine. The example provided below shows the features of flask that have been utilised for the application. This example code shows flask may be used to map URL's to controllers and return a view. This is very handle as different routes can be defined with this decorator to facilitate different functions dependent on the route. This is a fundamental feature when building applications on the web as it plays a significant role in user interaction and interface.

https://flask.palletsprojects.com/en/3.0.x/

#### Example code
```
@app.route('/')
def home():
    return 'Hello, World!'`
```

#### SQLAlchemy
SQLAlchemy is used within the game event tracking application to assist with database CRUD operations such as retrieving values from an entity within the relational database etc. It is also used within the database tables for attributes and data type definitions, commits to the database session and scalars for executing of the database object. This example shows ```db.Select``` is used to fetch an object from the model ```Games``` and return it to the view with the use of Marshmallow.

#### Example
```
@game_bp.route("/<int:game_id>", methods=["GET"])
def view_games(game_id):
    stmt = db.Select(Games).filter_by(id=game_id)
    game = db.session.scalar(stmt)

    if game:
        return game_schema.dump(game), 200
    else:
        return{"error": f"There is no game with id: {game_id}"}
```

##### flask_sqlalchemy
1. Install flask_sqlalchemy package

``` pip install flask_sqlalchemy```

#### Marshmallow
For this application marshmallow has been used to create my schemas and help with serialising and deserialising my python objects into a readable object for the view. It has also been used to help define the specific attributes that will be accessed by different tables as well as validation of inputs by the user - restricting users to certain inputs and conditions. 

An example of how marshmallow has been used extensively in my application has been provided below. 

##### Use within application
In this example I have used marshmallow to create a schema class model named ```GameSchema``` and used many of marshmallows features such as ```fields``` and ```validate```. Some methods of fields were used for different purposes. ```Nested``` was used to define which attributes from other tables were going to be availble for use, ```String``` was used for validating user input and ensuring user input is compulsory.

![Game-Marshmallow](./docs/GameSchema.PNG)

##### flask_marshmallow
1. Install flask_marshmallow package

``` pip install flask_marshmallow```

##### marshmallow_sqlalchemy
1. Install marshmallow_sqlalchemy package

``` pip install marshmallow_sqlalchemy```


#### JWT Manager
JWT Manager is a popular Flask extension that provides easy integration of JSON Web Tokens (JWT) into the game event tracker application. Within this application it enables management of user authentication and authorization and retrieval of attribute id's with the use of ```get_jwt_identity()``` for display in the view.

#### Example
```
@game_bp.route("/", methods=["POST"])
@jwt_required()
@check_admin
def create_game():
    request_data = request.get_json()
    name = request_data.get("name")
    description = request_data.get("description")
    stmt = db.Select(Users).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    game = Games(
        name = name,
        description = description,
        user_id = user.id
        )

    db.session.add(game)
    db.session.commit()
    return game_schema.dump(game), 201
```

##### flask_jwt_extended
1. Install flask_jwt_extended package

``` pip install flask_bcrypt```

#### Bcrypt
Bcrypt is used within this application for its cryptographic hashing function designed specifically for securely storing passwords input by the user into the database. The example below shows how bcrypt has been used in this application to hash the user input password into a database object. Bcrypt has also been used to verify user's when logging in by comparing the user input password to the stored hashed password to see if they are the same - this assists in authenticating users upon logging in with the application.

#### Example
```
  user.password = bcrypt.generate_password_hash(request_password).decode("utf-8") or user.password
```

##### flask_bcrypt
1. Install flask_bcrypt package

``` pip install flask_bcrypt```

## R4 - PostgreSQL
PostgresQL is a catalog-driven, object relational database management system (ORDBMS) that is open source and is popularly utilised by multiple users due to its diverse functionality, features, stability, dependability & efficient implementation. It supports relational and non-relational queries such as SQL and JSON respectively (The PostgreSQL Global Development Group, 2019). PostgreSQL stores data in tables columns and rows, whilst data is written and read using SQL language. A major variant of PostgreSQL in comparison to other relational database systems is the additional quantity of information stored such as; data types, access methods and functions, extending its routine storage of tables and columns in catalogs(Hassan, 2022). 

### Application
Its benefits range from its exceptional extensible nature and its consistent compliance to guidelines. With the use of functions such as MVCC, it is capable of concurrent database interactions within multi-user environments which will be further discussed below. 
(Kengalagutti, n.d.). PostgreSQL is known to be used as a DBMS in the financial industry, many industrial manufactures and works with multiple web frameworks such as Django and PHP(Peterson, 2019).

### Features 
PostgreSQL acts as a principal database for information throughout many applications, devices, the web and functions as software that enables reading, writing and modifying relational databases(Peterson, 2019). Its highly extensible nature allows for its use across multiple programming languages such as Ruby, Python and Java. Its multifaceted nature facilitates the creation of defined data types and customised functions. Another significant element of PostgreSQL is its conformance to standardised SQL requirements and a majority of features that are obligatory for SQL(Peterson, 2019). 

#### Data Definition Language (DDL)
Data definition is a feature of PostgreSQL that is involved in modifications, definitions & structuring of databases & schemas. Using DDL is useful in storing data within the database and altering the structural integrity of the database, such as making aliases, altering columns, dropping columns or creating tables (Commandprompt.com, 2023).

- Create Tables  
The statement ```'CREATE TABLE'``` will create a table within a database. Syntax of these statements ends with a ```;```. This specific example discussed will create a table named ```students``` with attributes ```Teacher_ID, Name, Subject``` with their respective datatypes and constraints(Awati, 2022).

``` 
CREATE TABLE students
(
  Teacher_ID INT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL,
  Subject VARCHAR(50) NOT NULL,
); 
```

- Alter Constraints or columns  
The statement ```ALTER TABLE``` will alter a database tables constraints or columns. Syntax involves ending these statements ends with a ```;```. This specific example discussed will alter a table named ```students``` by adding a column named ```column_name``` with data type ```data_type```(Awati, 2022).

```
ALTER TABLE students ADD column_name data_type;
```

##### DCL   
Delete command line (DCL) is a statement used to amputate multiple or singular record entries from existing tables within a database. The ```WHERE``` clause may be used to specify a row of the database table. This example deletes a data entry depending on the ```WHERE condition```
(AWS, 2024).
```
DELETE FROM table_name WHERE condition;
```

### Benefits of Using PostgreSQL
As one of the most popular databases, PostgreSQL has manifold benefits ranging from extensibility, reliability, scalability, ACID compliance & multiversion concurrency control to name a few(PostgreSQL Documentation, 2024). Elaborate optimisations with queries within larger data sets makes PostgreSQL a better alternative. Some key benefits that cement PostgreSQL's practicality will further be discussed below:

#### Multiversion concurrency control (MVCC)  
MVCC is a method to handle concurrency within PostgreSQL, used to enhance and optimise databases when numerous processes require the same database (devcenter.heroku.com, n.d.). It works on the basis of providing optimisation for multi-user environments by providing continual integrations of changes to databases eschewing locking mechanisms which are utilised by other database systems. This is completed through the utilisation of advanced techniques and multiversion models (PostgreSQL Documentation, 2012). MVCC utilises duplication to allow for simultaneous requests to read or write from or to the database respectively without any impediments. It provides a snapshot of data from a specific version independent of the current state of the primary data when a query is made, promoting transaction isolation(PostgreSQL Documentation, 2012). This is highly beneficial as it improves performance, user experience, facilitates simultaneous transactions and reduces inconsistencies & contentions with data retrieval, possibly due to concurrent processes that may occur (E.g Changes made in the database to a specific row will only affect a specific database version - snapshotted version of the data) (www.theserverside.com, n.d.). MVCC is greatly beneficial as it facilitates collaborations, agile work production & consistent data retrieval/alterations without contention (PostgreSQL Documentation, 2024).
 
#### Extensibility - PostGIS
PostgreSQL has a fundamental concept involving extending the use of database table operations for users, in comparison it is imperative for other standard database systems to change source code or load modules for extensible properties. Another variable in the benefits of PostgreSQL's extensibility lies in its automation capabilities via dynamic loading to incorporate pre-defined code by users into its own server (PostgreSQL Documentation, 2023). These capababilities substantiates PostgreSQL's benefits as a database and its utilisation whilst prototyping applications swiftly. Another notable extensible factor includes functionality with features such as PostGIS. PostGIS is open source and a spatial database that helps with database management by prompting indexation, querying and storage of geospatial data. This can include distances to the nearest pizza shop, specific points based on geographic location or the size of a country to name a few (Topi Tjukanov, 2018). This is greatly benefitial as an extension, expediting manipulation of geographic and geometric data within a database. Examples of where PostGis has been used includes:
various industries such as: Broadcast Media Production And Distribution, Defense and Space Manufacturing & Software Development. It's principal features includes:
- Spatial Functions
Geometric operations such as measurements of area and distance, spatial relationships dependent on containment and proximity help provide a wide range of uses in regards to spatial analysis tasks.
- Geometry Processing
Processing of spatial data in 3D and 4D geometrics. Urban planning, environmental modeling. 

#### Disaster Recovery 
Disaster Recovery is a substantial benefit when using PostgreSQL as a means of employing mechanisms to recover initial operational states and data in case something unexpected occurs (Percona LLC, 2024). 

##### Write-ahead Logging (WAL)
WAL is a method used as part of disaster recovery of content after a crash has occurred. This system assists in ensuring the integrity of data by logging alterations with table and index data prior to writing changes to those data files, these logs are recorded and flushed to disk. This apparatus supports the idea of roll-forward recovery (REDO), where database content may be recovered after a crash based on the logging of data(PostgreSQL Documentation, 2022). This log is stored in a subdirectory ```pg_wal```, recording subsequent changes made to database contents. WAL is also supported by different recovery methods such as point-in-time and on-line recovery, WAL data may be archived for use when reverting to a particular point in time by backing up of database contents physically(PostgreSQL Documentation, 2022).

##### pgBackRest 
Opensource program used for its reliability in backing up PostgreSQL databases after hardware failure to recover database clusters at points in time utilising methods such as full or delta restore to restore data. An empty directory is required for a full restore whereas a delta recovery will recognise pre-existing files and make changes to only the files the backup contains (pgBackRest - Reliable PostgreSQL Backup & Restore, 2024). A common scenario where pgBackRest may be applied would be corrupted or lost data - restoring the database to a previous functioning state where a live database cluster will be started as a result(pgBackRest - Reliable PostgreSQL Backup & Restore, 2024). pgBackRest provides configurations to backup and restore data, a beneficial solution towards PostgreSQL databases. It include multiple functionalities ranging from remote or local operations, differing backup types such as; Full, Differential or Incremental & backup integrity to name a few (pgBackRest - Reliable PostgreSQL Backup & Restore, 2024). These features will be briefly discussed below:

It can provide many of the following solutions when restoring database content:
- Full Backup
pgBackRest copies a complete snapshot of database content to a backup for later use in recovery of database cluster(Crunchy Data, 2019).  
- Differential Backup
This process of storing the differential backup involves pgBackRest copying changed database files since the last full backup to a differential backup. pgBackRest will then copy files for restoration from the differential backup as well as suitable database cluster files from the full backup prior (Crunchy Data, 2019).
- Incremental Backup
pgBackRest will backup any file changes since the last full or differential backup. Incremental backups depend on both full and differential backups to be valid to restore (Crunchy Data, 2019). 

### Cons of Using PostgreSQL
#### Slower performance
Due to PostgreSQL analysing relational database structures line-by-line starting from the first occurence of a row to find relevant content, this slows the processing time in large database sets as it requires comparison of additional fields.(Stuti Dhruv, 2019) In comparison to MySQL, plain operations involving read and write tend to be slower (Kengalagutti, n.d.). The speed of indexed database tables with PostgreSQL was seen to be much slower with execution time in comparison to MySQL on a tenfold increasing scale, implying each index column required additional time for inserting into database tables. Other databases such as MySQL are seen to be significantly much faster in performance of CRUD operations such as select, update and remove when it comes to indexed MySQL databases, representing a constant time for completion. This further solidifies the performance related issues of PostgreSQL and highlights the need for uses of other RDBMS depending on user specific applications(IONOS editorial team, 2022). 

#### Setup and Maintaining Complexity
Setting up and configuring PostgreSQL has a steep learning curve due to its robust wealth of features and in turn setting up and optimisation may become difficult in comparison to simpler database systems like MySQL(IONOS editorial team, 2022). Associations with new customers when using PostgreSQL necessitates the assignment of increasing memory for subsequential customer associations, this can lead to a rapid increase in memory usage for databases resulting in a net negative consequence in terms of computational efficiency. In contrast to other RDBMS such as MySQL, the overall number of database directors is also lesser in terms of experience with use of PostgreSQL further emphasising its complexity (Kengalagutti, n.d.).


### Example on how PostgreSQL is used and installed to create a database
1. Install PostgreSQL
```
pip install postgres
```

2. Run PostgreSQL

Mac
```
psql
```

Linux 
```
sudo -u postgres psql
```

3. Creating Database

```
CREATE DATABASE <database_name>
```

4. Showing a list of Databases

\l

5. Connect to Database <database_name> 
```
\c <database_name> 
```
(Microfocus.com, 2018)

## R5 - SQLAlchemy (ORM)
SQLAlchemy is a popular Object-Relational Mapping (ORM) library for Python, providing a high-level abstraction for working with relational databases by acting as a mediator between python application code and the relational database, facilitating interactions between the two without the use of SQL queries. SQLAlchemy helps with querying the database through the utilisation of python class conversions to SQL statements. SQLAlchemy has a multitude of features ranging from CRUD operations, class mapping, defining of foreign keys, relationships, attributes and datatypes. Some of these key features will be discussed below.

https://datascientest.com/en/sqlalchemy-what-is-it-whats-it-for
https://www.sqlalchemy.org/

### Features 
#### CRUD Operations
A key feature with the use of SQLAlchemy's ORM layer is the ability to perform CRUD operations. This includes the creation, reading, updating and deleting of data in the database. This is essential as users provide input from the front-end, these user inputs may interact with the database and be stored for later retrieval, analysis or deletion. This specific example shows the ability for SQLAlchemy to provide a view back to the user.
1. A decorator is used containing an endpoint and HTTP request method
2. A controller function is defined
3. Using a method from SQLAlchemy the specific database object is fetched
4. A schema of the game is returned to the user with an appropriate error code. If there is no such specific game an error message is provided to the user.

An example of how CRUD operations may be used in application can be seen below: 

#### Example - CRUD Operations

```
@game_bp.route("/<int:game_id>", methods=["GET"])
def view_games(game_id):
    stmt = db.Select(Games).filter_by(id=game_id)
    game = db.session.scalar(stmt)

    if game:
        return game_schema.dump(game), 200
    else:
        return{"error": f"There is no game with id: {game_id}"}
```
#### Defining database models
With the ORM layer implemented within SQLAlchemy, a key feature would be the definition of database models. This is done by:
1. Create object instance of SQLAlchemy - for this example db is the object instance and has been created in an init.py file and imported as db.
2. Defining the database model includes creating of a class with the ```<model_name>``` followed by ```db.Model``` passed as a parameter. 
3. The table name needs to be defined using ```__tablename__```.
4. Each attribute will be defined with the ```<attribute_name>``` followed by ```db.Column``` and definitions of its data type and constraints. E.g; ```db.Integer```, ```nullable=False```.

#### Relationships
Anothey key feature with the use of SQLAlchemy ORM is its ability to relate entities to one another with the use of ```db.relationship```.
1. Following on from "Defining database models", the table that needs to be linked will be specified. In this example ```games```.
2. ```games``` will be assigned a ```db.Relationship``` where it will be preceded by the ```<model_name>``` and a method namely ```back_populates```.
3. ```<model_name>``` will be provided the value of the model needing to be linked to, ```back_populates``` will be provided a value relating to the  relationship between the two tables. In this example "user" is provided as the relationship between user and games is One-to-Many relationship. One user can make multiple games, although a game can only be made by one user. 

#### Foreign Keys
Foreign keys is another feature which can also be defined to provide more detail on the relationship type between entities. This example shows SQLAlchemy can be used to link the users primary key named ```id``` to the table ```Games```. 

### Example Code - Foreign Keys
```
class Games(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.Relationship("Users", back_populates="games")
    players = db.Relationship("Players", back_populates="game")
```

### Example Code - Defining database models + Relationships


```
from init import db,ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    is_authorised = db.Column(db.Boolean, default=False)

    games = db.Relationship("Games", back_populates="user")
```


## R6 - Normalised database relations
- Eliminate redundancy and inconsistenct dependencies
- Eliminate repeating groups in individual tables.
- Create a separate table for each set of related data.
- Identify each set of related data with a primary key.
- Create separate tables for sets of values that apply to multiple records.
- Relate these tables with a foreign key.
- Eliminate fields that don't depend on the key.

### How Normalisation occurs in project
Each divisible attribute has been provided its own table to rely solely on its own primary key. 

#### 1NF - First Normal Form
- [x] All columns contain atomic (indivisible) values
- [x] Each entry in a column is of the same data type.
- [x] Each column has a unique name.
- [x] The order in which data is stored does not matter.

#### 2NF - Second Normal Form
- [x] All non-key attributes are fully functionally dependent on the primary key (no partial dependency).

#### 3NF - Third Normal Form
- [x] There are no transitive dependencies (non-key attributes should not depend on other non-key attributes).

### ERD
![Crows-Foot-Notation](./docs/ERDT2A2.drawio.png)

### Other levels of normalisation - Model: User

### Key/Legend
#### Entity 
A rectangle representing a data entity (e.g., User, Order, Product).


#### Attribute	
An oval connected to an entity, representing a property of that entity (e.g., name, price).

#### Primary Key	
An underlined attribute that uniquely identifies each record within an entity.

#### Foreign Key	
An attribute that references the primary key of another entity, often shown with a dashed line.

#### Crow's Foot	
A symbol that indicates the "many" side of a relationship, represented by three lines.

#### Single Line	
Indicates a "one" relationship, meaning that each instance of an entity can be associated with only one instance of another entity.

#### Double Line	
Indicates a mandatory relationship, where an instance of one entity must be associated with at least one instance of another entity.

#### Zero or One	
A circle at the end of a line that indicates the possibility of having no related instance in the relationship.

#### One or Many	
A combination of a line and a Crow's Foot symbol that shows that an instance may have zero or more related instances.

#### Relationship Name	
A diamond shape that describes the nature of the relationship between entities (e.g., places, contains).



## R7
### Users  
The users model was created to help define the attributes and each data type, constraint and relationship with other models (Games model). It was also created with validation methods included within marshmallows module validate to ensure users enter appropriate inputs from the front end. The Users model was also created to keep in mind of allowing or denying access to creating, 
updating or deleting games - this is part of othe user controller. Only users that are authorised with a true value for ```is_authorised``` are allowed to create, update and delete games. Users that do not have these access rights are only able to view games. 

The users model will include the following components:  

#### Attributes
- **id**: Used as the primary key for the users table, integer type
- **name**: Used to define the users name, string type, cant be left empty by front end input
- **password**: Used to define user password, string type, cant be left empty by front end input
- **email**: Used to define user email, string type, cant be left empty by front end input
- **is_authorised**: Used to define admin rights, boolean type, if user leaves empty default value is False
  
#### Schema  

The users schema will include the following components:  
- **Meta**: 
  - **fields**: Fields helps define the atttributes that will be required from the users model
- **games**: used to define the certain attributes to share from the games table to the users table. Exclude was included to prevent schema including the user component to the users table.
- **name**: used in schema to help with validating user input. Name must only contain characters A-Z.
- **password**: used in schema to help with validating user input. Password must contain at least one letter, one digit, and is between eight and sixteen characters in length.
- **email**: used in schema to help with validating user input. Email must contain @ symbol followed and preceding non white space characters.

#### Code Example   
![User-Model](./docs/User.PNG)

#### User-Games Relationship:
The relationship between User and Games is a One-to-Many relationship. One user can create multiple games although one game has to be created by a user. The foreign key will be assigned to the Games table referenced from the primary key associated to the user table. The user model interacts with the games model through the use of ```games = db.Relationship("Games", back_populates="user")```. This creates the relationship between the games and users table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.
#### Queries to access data using relationships:

- **Create**:   
Query to create a game from user input, the game will include the user attributes; name, email, id and is_authorised when displayed in the view to the user using the game_schema. 
```
@game_bp.route("/", methods=["POST"])
@jwt_required()
@check_admin
def create_game():
    request_data = request.get_json()
    name = request_data.get("name")
    description = request_data.get("description")
    stmt = db.Select(Users).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    game = Games(
        name = name,
        description = description,
        user_id = user.id
        )

    db.session.add(game)
    db.session.commit()
    return game_schema.dump(game), 201
```

- **View**:  
- Query to view a specific game from user input, the game will include the user attributes; name, email, id and is_authorised when displayed in the view to the user using the game_schema. 
```
@game_bp.route("/<int:game_id>", methods=["GET"])
def view_games(game_id):
    stmt = db.Select(Games).filter_by(id=game_id)
    game = db.session.scalar(stmt)

    if game:
        return game_schema.dump(game), 200
    else:
        return{"error": f"There is no game with id: {game_id}"}
```

### Games
The Games model was created to help with bridging a relationship between the games that are created and players associated to each game. The games model defines the games primary key, name of the game, description of the game and includes a foreign key referenced from the users model. It also has relationships with both the users model and players model. 

The games model will include the following components:

#### Attributes

- **id**: Defines the games primary key
- **name**: Defines the games name
- **description**: Defines the games description
- **user_id**: Defines the foreign key referenced from the users model
- **user**: Defines the relationship between the users model and the games model
- **players**: Defines the relationship between the players model and the games model

#### Schema

The games schema will include the following components:  
- **Meta**: 
  - **fields**: Fields helps define the atttributes that will be required from the games model
- **games_schema/game_schema**: used to help handle single or multiple user objects. E.g if fetching multiple games to view ```games_schema``` would be used, if fetching only 1 game to view ```game_schema``` would be used.
- **user**: used to define the certain attributes to share from the users table to the games model. Exclude was included to prevent schema including specific user attributes to the games table.
- **players**: used to define the attributes to exclude from the playerschema for sharing to the games model.
- **name**: used for validation of user input from front-end, accepting letters ONLY from 1-40 characters max.
- **description**: used for validation of user input from front-end, accepting letters ONLY from 1-40 characters max.

#### Code Example
![Game-Model](./docs/Game.PNG)

#### Games-User Relationship:
The relationship between Games and Users is a Many-to-One relationship. One user can create multiple games although one game has to be created by a user. The foreign key will be assigned to the Games table referenced from the primary key associated to the user table. 

- The game model interacts with the user model through the use of ```  user = db.Relationship("Users", back_populates="games")```. This creates the relationship between the games and users table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.

#### Game-Players Relationship:
The relationship between Games and Players is a One-to-Many relationship. One game can have multiple players although one player has to be associated only to one game. The foreign key will be assigned to the Players table referenced from the primary key associated to the games table. 

- The game model interacts with the player model through the use of ``` players = db.Relationship("Players", back_populates="game")```. This creates the relationship between the games and players table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.

##### Queries
- Create
POST HTTP request is used to create a player based on user input. The view will return the game the player is associated to. 
```
@player_bp.route("/", methods=["POST"])
def create_player(game_id):
    # Retrieve JSON data from the request
    request_data = request.get_json()
    body_name = request_data.get("name")

    # Validate required fields
    # if not name or date or role:
    #     return{"error": "Name, date & role are required"}, 400

    # Check if the name is already in use
    player_stmt = db.Select(Players).filter_by(name=body_name)
    existing_user = db.session.scalar(player_stmt)
    if existing_user:
        return{"error": "Name already in use"}, 400

    else:
    # Create a new Player instance
        stmt = db.Select(Games).filter_by(id=game_id)
        game = db.session.scalar(stmt)
        player = Players(
                name= body_name,
                date= request_data.get("date"),
                role= request_data.get("role"),
                game_id = game.id
            )

        token = create_access_token(identity=str(player.id), expires_delta=timedelta(days=1))

        # Add and commit the new player to the database
        # try:
        db.session.add(player)
        db.session.commit()

    # Return the newly created player's data
    return player_schema.dump(player), 201

```

- View
GET HTTP request used to fetch all players from the database. The view returned will also return certain attributes from the games tables as well as attributes from the players tables.

```
@player_bp.route("/", methods=["GET"])
def view_players(game_id):
    stmt = db.select(Players)
    player = db.session.scalars(stmt)

    if player:
        return players_schema.dump(player), 201
    else:
        return {"error" : "There are no players to show"}
```


### Players
Players model includes the following components:

#### Attributes
- **id**: Defines primary key
- **name**: Defines players name
- **date**: Defines date player was created
- **role**: Defines the players role in the game
- **game_id**: Defines the foreign key referenced from the games model
- **game**: Defines the relationship between the games model and the players model
- **events**: Defines the relationship between the players model and the events model
- **comments**: Defines the relationship between the players model and the comments model

#### Player Schema

The players schema will include the following components:  
- **Meta**: 
  - **fields**: Fields helps define the atttributes that will be required from the players model
- **games_schema/game_schema**: used to help handle single or multiple user objects. E.g if fetching multiple players to view ```players_schema``` would be used, if fetching only 1 game to view ```player_schema``` would be used.
- **game**: used to define the certain attributes to share from the games schema to the players schema. 
- **events**: used to define the attributes to include from the events schema for sharing to the players schema.
- **comments**: used to define the attributes to include from the comments schema for sharing to the players schema.
- **name**: used for validation of user input from the front-end, name can only be letters from 1-50 characters max.

- **Players-Games Relationship**:
The relationship between Players and Games is a Many-to-One relationship. One game can have multiple players although each player has to be created for one game. The foreign key will be assigned to the Players table referenced from the primary key associated to the game table. 

- The players model interacts with the game model through the use of ```game = db.Relationship("Games", back_populates="players")```. This creates the relationship between the players and games table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.
- foreign keys will be passed with ```game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)``` to assign the foreign key to the players model referenced from the games model's id.

- **Players-Comments Relationship**:
The relationship between Players and comments is a One-to-Many relationship as One player can have multiple comments but a comment can only be made by a player. The foreign key will be assigned to the comments table referenced from the primary key associated to the player table.

- The players model interacts with the comments model through the use of ```comments = db.Relationship("Comments", back_populates="player")```. This creates the relationship between the players and comments table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.

- **Players-Events Relationship**:
The relationship between Players and events is a One-to-Many relationship as One player can create multiple events but an event can only be made by a player. The foreign key will be assigned to the events table referenced from the primary key associated to the player table.

- The players model interacts with the events model through the use of ```events = db.Relationship("Events", back_populates="player")```. This creates the relationship between the players and events table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.

##### Queries
- Create Player
Using HTTP request method POST to create a player based on json body input from the front-end. This will create a new object instance of a player which also links the games attributes.

- View Players
Using HTTP request method GET to fetch players from the database and provide a list of players back to the view for the user to see.

```
@player_bp.route("/", methods=["GET"])
def view_players(game_id):
    stmt = db.select(Players)
    player = db.session.scalars(stmt)

    if player:
        return players_schema.dump(player), 201
    else:
        return {"error" : "There are no players to show"}
```

### Events

#### Events-Comments Relationship
This is a One-to-Many relationship where the foreign key is added to the comments table referencing the primary key id of the event entity. This is because one event can have multiple comments but a comment can only be a part of one event.

- The events model interacts with the comments model through the use of ```comments = db.Relationship("Comments", back_populates="event")```. This creates the relationship between the events and comments table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.

#### Events-Player Relationship
The relationship between events and players is a Many-to-One relationship. One event is assigned to a player but one player can create multiple events. The foreign key will be assigned to the events table referenced from the primary key associated to the players table. 

- The events model interacts with the player model through the use of ```player = db.Relationship("Players", back_populates="events")```. This creates the relationship between the events and players table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.

#### Events-Category Relationship
The relationship between events and players is a One-to-Many relationship. One event can be a part of multiple categories whereas one category must be a part of one event. The foreign key will be assigned to the category table referenced from the primary key associated to the events table. 

- The events model interacts with the category model through the use of ```categories = db.Relationship("Category", back_populates="event")```. This creates the relationship between the events and category table so that both models will be able to interact with each other models attributes - the schema will define which specific attributes are needed by the other model for CRUD operations.

### Queries

#### Comments

- User-Games Relationship:
The relationship between User and Games is a One-to-Many relationship. One user can create multiple games although one game has to be created by a user. The foreign key will be assigned to the Games table referenced from the primary key associated to the user table. 
- Interaction with other models:
- Queries to access data using relationships:
- Code Examples:

#### Records
- Description:

- User-Games Relationship:
The relationship between User and Games is a One-to-Many relationship. One user can create multiple games although one game has to be created by a user. The foreign key will be assigned to the Games table referenced from the primary key associated to the user table. 
- Interaction with other models:
- Queries to access data using relationships:
- Code Examples:

#### Category
- Description:

- User-Games Relationship:
The relationship between User and Games is a One-to-Many relationship. One user can create multiple games although one game has to be created by a user. The foreign key will be assigned to the Games table referenced from the primary key associated to the user table. 
- Interaction with other models:
- Queries to access data using relationships:
- Code Examples:


#### Games

#### Players

#### Comments

#### Records

#### Events

#### Category

## R8 - API Endpoints
### User Controller


## Styling Guide - API style guide
ALL queries or model methods are commented to a THOROUGH level of detail, with reference to a style guide or comment style guide in the project documentation.

https://docs.gitlab.com/ee/development/api_styleguide.html