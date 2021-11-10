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
DATABASE_FILE = "userData_database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s?check_same_thread=False'%(DATABASE_FILE), echo = False) 

Base = declarative_base()

##CLASSES##

class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    code = Column(String)
    time_stamp = Column(DateTime)
    def __repr__(self):
        return "<User(id=%s code='%s', time_stamp='%s')>" % (
                                self.id, self.code, str(self.time_stamp))
    def as_json(self):
        return {
            'id':self.id,
            'code':self.code,
            'time_stamp':self.time_stamp,
        }

class OpenGate(Base):
    __tablename__ = 'opengate'
    user_id = Column(String, primary_key=True)
    gate = Column(String)
    time_stamp = Column(DateTime)
    def __repr__(self):
        return "<User(user_id=%s gate='%s', time_stamp='%s')>" % (
                                self.id, self.code, str(self.time_stamp))
    def as_json(self):
        return {
            'user_id':self.id,
            'gate':self.code,
            'time_stamp':self.time_stamp,
        }

Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

def newUser(ID,code,time):
    user = User(id = ID,code = code,time_stamp = time)
    session.add(user)
    session.commit()

def getUserById(ID):
    resp = session.query(User).filter(User.id == ID).first()
    return resp

def setNewUserCode(ID, newCode, newDate ):
    user=getUserById(ID)  
    if bool(user):  
        user.code = newCode
        user.time_stamp = newDate
        session.commit()
   

# def validateCode(ID,code,gate_id):
#     resp = getUserById(ID)
#     true1 = str(resp.code) == code
#     true2 = resp.time_stamp + timedelta(minutes = 2)  > datetime.datetime.now()
#     if str(resp.code) == code and resp.time_stamp + timedelta(minutes = 2)  > datetime.datetime.now():
#         resp.time_stamp =  datetime.datetime.now() - timedelta(weeks = 100)
#         gate = getGateById(gate_id)
#         gate.count = gate.count + 1
#         session.commit()
#         return 0
#     elif str(resp.code) == code and (resp.time_stamp < datetime.datetime.now() - timedelta(weeks = 50)):
#         return 2 #code has already been used
#     else:
#         return 1