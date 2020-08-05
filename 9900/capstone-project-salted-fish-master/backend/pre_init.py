#!/usr/bin/python3

'''
IMPORTANT:
This script will drop all tables in database and re-create it, which means
that all existing data will be deleted.
Use with CAUTION!
'''

from db import DB
import yaml
from users.admin import Admin
from users.collaborator import Collaborator
from users.dreamer import Dreamer

# load server config
print("Read server configuration")
f = open('server.config', 'r', encoding='utf-8')
config = yaml.load(f.read(), Loader=yaml.FullLoader)

print("Start database pre initialisation")
db = DB()
conn = db.conn()
print("default database connection established")

print("======= clean all existing tables =======")

print("discussion")
query = 'drop table if exists discussion;'
conn.execute(query)

print("subscription")
query = 'drop table if exists subscription;'
conn.execute(query)

print("dreamer_notification")
query = 'drop table if exists dreamer_notification;'
conn.execute(query)

print("collaborator_notification")
query = 'drop table if exists collaborator_notification;'
conn.execute(query)

print("skills")
query = 'drop table if exists skills;'
conn.execute(query)

print("application")
query = 'drop table if exists application;'
conn.execute(query)

print("invitation")
query = 'drop table if exists invitation;'
conn.execute(query)

print("role_skill")
query = 'drop table if exists role_skill;'
conn.execute(query)

print("project_role")
query = 'drop table if exists project_role;'
conn.execute(query)

print("project")
query = 'drop table if exists project;'
conn.execute(query)

print("admin")
query = 'drop table if exists admin;'
conn.execute(query)

print("collaborator")
query = 'drop table if exists collaborator;'
conn.execute(query)

print("dreamer")
query = 'drop table if exists dreamer;'
conn.execute(query)


print("======= rebuild tables =======")
# admin table
print("rebuild admin table...")
query = '''CREATE TABLE admin (
ID INT(11) NOT NULL AUTO_INCREMENT,
name VARCHAR(50) DEFAULT NULL,
email VARCHAR(256) DEFAULT NULL,
password VARCHAR(64),
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
UNIQUE KEY (`email`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# collaborator table
print("rebuild collaborator table...")
# education: -1 = default, 1 = Other, 2 = bachelor, 3 = master, 4 = PhD
query = '''CREATE TABLE collaborator (
ID INT(11) NOT NULL AUTO_INCREMENT,
name VARCHAR(50) DEFAULT NULL,
email VARCHAR(256) DEFAULT NULL,
password VARCHAR(64),
phone_no VARCHAR(20) DEFAULT NULL,
education TINYINT DEFAULT -1,
user_level INT(5), description TEXT,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`),
UNIQUE KEY (`email`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# dreamer table
print("rebuild dreamer table...")
query = '''CREATE TABLE dreamer (
ID INT(11) NOT NULL AUTO_INCREMENT,
name VARCHAR(50) DEFAULT NULL,
email VARCHAR(256) DEFAULT NULL,
password VARCHAR(64),
phone_no VARCHAR(20) DEFAULT NULL,
user_level INT(5),
description TEXT,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`),
UNIQUE KEY (`email`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# skill/exp table
print("rebuild skill/exp table...")
query = '''CREATE TABLE skills (
skill TINYINT DEFAULT -1,
experience TINYINT DEFAULT 0,
collaboratorID int(11) NOT NULL,
FOREIGN KEY (`collaboratorID`) REFERENCES collaborator(`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# Always create No.1 collaborator/dreamer/admin for system keeping to avoid foreign key error
print("create No.1 user as admin from config")
new_admin = Admin(config['Admin']['Name'], config['Admin']['Email'], config['Admin']['Password']).commit(conn)
new_collab = Collaborator(config['Admin']['Name'], config['Admin']['Email'], config['Admin']['Password']).commit(conn)
new_dreamer = Dreamer(config['Admin']['Name'], config['Admin']['Email'], config['Admin']['Password']).commit(conn)

# project table
print("rebuild project table...")
query = '''CREATE TABLE project (
ID INT(11) NOT NULL AUTO_INCREMENT,
project_title VARCHAR(100) DEFAULT NULL,
description TEXT DEFAULT NULL,
category TINYINT DEFAULT -1,
dreamerID int(11) NOT NULL,FOREIGN KEY (`dreamerID`) REFERENCES dreamer(`ID`),
project_status TINYINT DEFAULT 1,
is_hidden TINYINT DEFAULT 0,
hidden_reason VARCHAR(256) DEFAULT NULL,
is_modified_after_hidden TINYINT DEFAULT 0,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# project_role table
print("rebuild project_role table...")
query = '''CREATE TABLE project_role (
ID INT(11) NOT NULL AUTO_INCREMENT,
projectID int(11) NOT NULL, FOREIGN KEY (`projectID`) REFERENCES project(`ID`),
title VARCHAR(50) DEFAULT NULL,
amount INT(3) DEFAULT NULL,
education TINYINT DEFAULT -1,
general_enquiry VARCHAR(2048) DEFAULT NULL,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# role_skill table
print("rebuild role_skill table...")
query = '''CREATE TABLE role_skill (
skill TINYINT DEFAULT -1,
experience TINYINT DEFAULT 0,
roleID int(11) NOT NULL,
FOREIGN KEY (`roleID`) REFERENCES project_role(`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# application table
print("rebuild application table...")
query = '''CREATE TABLE application(
ID INT(11) NOT NULL AUTO_INCREMENT,
projectID int(11) NOT NULL,FOREIGN KEY (`projectID`) REFERENCES project(`ID`),
role_applied int(11) NOT NULL,FOREIGN KEY (`role_applied`) REFERENCES project_role(`ID`),
applicant int(11) NOT NULL,FOREIGN KEY (`applicant`) REFERENCES collaborator(`ID`),
status TINYINT DEFAULT -1,
general_text TEXT DEFAULT NULL,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# invitation table
print("rebuild invitation table...")
query = '''CREATE TABLE invitation(
ID INT(11) NOT NULL AUTO_INCREMENT,
projectID int(11) NOT NULL,FOREIGN KEY (`projectID`) REFERENCES project(`ID`),
role_invited int(11) NOT NULL,FOREIGN KEY (`role_invited`) REFERENCES project_role(`ID`),
invitor int(11) NOT NULL,FOREIGN KEY (`invitor`) REFERENCES dreamer(`ID`),
invitee int(11) NOT NULL,FOREIGN KEY (`invitee`) REFERENCES collaborator(`ID`),
status TINYINT DEFAULT -1,
general_text TEXT DEFAULT NULL,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# discussion table
print("rebuild discussion table...")
query = '''CREATE TABLE discussion(
ID INT(11) NOT NULL AUTO_INCREMENT,
projectID INT(11) NOT NULL,FOREIGN KEY (`projectID`) REFERENCES project(`ID`),
parent_discussion_ID INT(11) DEFAULT NULL, FOREIGN KEY (`parent_discussion_id`) REFERENCES discussion(`ID`),
text TEXT DEFAULT NULL,
is_dreamer TINYINT DEFAULT 0,
d_author INT(11),FOREIGN KEY (`d_author`) REFERENCES dreamer(`ID`),
c_author INT(11),FOREIGN KEY (`c_author`) REFERENCES collaborator(`ID`),
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# subscription table
print("rebuild subscription table...")
query = '''CREATE TABLE subscription(
projectID INT(11) NOT NULL,FOREIGN KEY (`projectID`) REFERENCES project(`ID`),
is_dreamer TINYINT DEFAULT 0,
d_subscriber INT(11),FOREIGN KEY (`d_subscriber`) REFERENCES dreamer(`ID`),
c_subscriber INT(11),FOREIGN KEY (`c_subscriber`) REFERENCES collaborator(`ID`),
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# dreamer_notification table
print("rebuild dreamer_notification table...")
query = '''CREATE TABLE dreamer_notification(
ID INT(11) NOT NULL AUTO_INCREMENT,
dreamer_ID INT(11) NOT NULL,FOREIGN KEY (`dreamer_ID`) REFERENCES dreamer(`ID`),
notification_text TEXT DEFAULT NULL,
is_viewed TINYINT DEFAULT 0,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

# collaborator_notification table
print("rebuild collaborator_notification table...")
query = '''CREATE TABLE collaborator_notification(
ID INT(11) NOT NULL AUTO_INCREMENT,
collaborator_ID INT(11) NOT NULL,FOREIGN KEY (`collaborator_ID`) REFERENCES collaborator(`ID`),
notification_text TEXT DEFAULT NULL,
is_viewed TINYINT DEFAULT 0,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)) ROW_FORMAT=DYNAMIC;'''
conn.execute(query)

print("pre initialisation complete")
