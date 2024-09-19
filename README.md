# T2A2 API WebServer

## R1
### Explain Solved Problem
With the increasing popularity of games, the management and analysis of past in-game events becomes increasingly more significant as the player base and complexities of games evolve. A common denominator within most games is the absence of in-game event tracking whereby players have a way to execute events but they do not have a way to review each past event committed. Having an event tracker can help players review any changes to their characters and track the progressive development of characters on an ongoing basis, this can help prevents users from spending far too much time on the game if they have progressed a certain amount and for users that are forgetful, they're able to account for what they previously did with their players. 
### Explain How
This app works by using




## R2



## R3
### Dependencies 
An extensive explanation of each dependency used in this application can be found below:
> Prior to installation of each package users should work in a virtual environment to prevent conflictions with other project dependency versions:

### Installation:
#### Virtual Environment
1. Setup virtual environment

```python3 -m venv venv```

2. Activate the virtual environment

``` source venv/bin/activate```

#### Psycopg2
1. Install psycopg2 package

``` pip install psycopg2-binary```

#### Flask
##### flask_sqlalchemy
1. Install flask_sqlalchemy package

``` pip install flask_sqlalchemy```

##### flask_marshmallow
1. Install flask_marshmallow package

``` pip install flask_marshmallow```

##### flask_jwt_extended
1. Install flask_jwt_extended package

``` pip install flask_bcrypt```

#### marshmallow_sqlalchemy
1. Install marshmallow_sqlalchemy package

``` pip install marshmallow_sqlalchemy```

#### flask_bcrypt
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
SQLAlchemy is a popular Object-Relational Mapping (ORM) library for Python, providing a high-level abstraction for working with relational databases. It simplifies database interactions by allowing you to work with Python objects instead of raw SQL queries. 

https://www.sqlalchemy.org/

### Features 
#### Declarative Mapping
- Define your database schema using Python classes. The ORM’s declarative base class allows you to define mappings in a clear and Pythonic way.
    - **Class and Table Mapping** :
    - **Column Mapping** : Map class attributes to table columns

#### Migration Tools 
SQLAlchemy integrates with migration tools like Alembic to handle database schema changes and versioning. Alembic allows you to generate and apply migration scripts for schema evolution.

#### Custom Types and Adapters
Define custom data types and adapt them for use with SQLAlchemy. This is useful for handling special types of data or integrating with non-standard database types.

#### Transaction Isolation and Control
Control transaction isolation levels and manage transactions manually if needed.

#### Async Support
SQLAlchemy provides support for asynchronous programming using async/await syntax. This is particularly useful for applications that require high concurrency and performance.

#### Type Decorators
Create custom type decorators to modify how SQLAlchemy interacts with specific data types, providing more control over data serialization and deserialization.


#### Integration with Other Tools
##### Integration with Web Frameworks
SQLAlchemy integrates well with popular web frameworks like Flask and Django. For Flask, SQLAlchemy provides Flask-SQLAlchemy, a Flask extension that simplifies integration.

##### Compatibility
SQLAlchemy works with a wide range of databases, including PostgreSQL, MySQL, SQLite, Oracle, and SQL Server. It also supports various database-specific features and optimizations.

### Benefits

1hr 37mins

### Cons

### Functionalities

### Examples


## R6 - Normalised database relations

## R7

## R8

## Styling Guide
ALL queries or model methods are commented to a THOROUGH level of detail, with reference to a style guide or comment style guide in the project documentation.
