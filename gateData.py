from logging import PlaceHolder
from flask.json import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from os import path
import datetime
from datetime import timedelta


from sqlalchemy.sql.sqltypes import DateTime

#SLQ access layer initialization
DATABASE_FILE = "database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s?check_same_thread=False'%(DATABASE_FILE), echo = False) 

Base = declarative_base()

##CLASSES##