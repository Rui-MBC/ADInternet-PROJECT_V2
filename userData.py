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
    secret = Column(String)
    time_stamp = Column(DateTime)
    def __repr__(self):
        return "<User(id=%s code='%s',token='%s', time_stamp='%s')>" % (
                                self.id, self.code,self.secret, str(self.time_stamp))
    def as_json(self):
        return {
            'id':self.id,
            'code':self.code,
            'secret':self.secret,
            'time_stamp':self.time_stamp,
        }

class OpenGate(Base):
    __tablename__ = 'opengate'
    id =  Column(Integer, primary_key=True)
    user_id = Column(String)
    gate = Column(String)
    time_stamp = Column(DateTime)
    def __repr__(self):
        return "<User(id = %s user_id=%s gate='%s', time_stamp='%s')>" % (
                                self.id, self.user_id,self.gate, str(self.time_stamp))
    def as_json(self):
        return {
            'id':self.id,
            'user_id':self.id,
            'gate':self.gate,
            'time_stamp':self.time_stamp,
        }

Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

def newUser(ID,CODE,SECRET,TIME):
    user = User(id = ID,code = CODE,secret=SECRET,time_stamp = TIME)
    session.add(user)
    session.commit()

def getUserById(ID):
    resp = session.query(User).filter(User.id == ID).first()
    return resp
    
def getHistoryById(ID):
    resp = session.query(OpenGate).filter(OpenGate.user_id == ID).all()
    return resp


def setNewUserCode(ID, newCode, newDate ):
    user=getUserById(ID)  
    if bool(user):  
        user.code = newCode
        user.time_stamp = newDate
        session.commit()

def setNewUserSecret(ID, newSecret):
    user=getUserById(ID)  
    if bool(user):  
        user.secret = newSecret
        session.commit()
   
def newOpenGate(userId, gateId, timeStamp ):
    newOpen = OpenGate(user_id = userId,gate = gateId,time_stamp = timeStamp)
    session.add(newOpen)
    session.commit()

def history_list(user):
    ret_list = []
    lv = getHistoryById(user)
    for v in lv:
        vd = v.as_json()
        ret_list.append(vd)
    return ret_list

def validateCode(ID,code):
    resp = getUserById(ID)
    if not resp:
            resp = {
                'errorCode' : 3,
                'errorDescription':'this user does not exist.'
            }
            return resp
    #print(resp.code, resp.id)
   # true1 = str(resp.code) == code
    #true2 = resp.time_stamp + timedelta(minutes = 2)  > datetime.datetime.now()
    if str(resp.code) == code and resp.time_stamp + timedelta(minutes = 2)  > datetime.datetime.now():
        resp.time_stamp =  datetime.datetime.now() - timedelta(weeks = 100)
#         gate = getGateById(gate_id)
#         gate.count = gate.count + 1
        session.commit()
        resp = {
                'errorCode' : 0,
                'errorDescription':'Success'
            }
            
    elif str(resp.code) == code and (resp.time_stamp < datetime.datetime.now() - timedelta(weeks = 50)):
        resp = {
                'errorCode' : 2,
                'errorDescription':'code has already been used.'
            }
    else:
        resp = {
                'errorCode' : 1,
                'errorDescription':'wrong code.'
            }
    return resp