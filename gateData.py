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
DATABASE_FILE = "gateData_database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s?check_same_thread=False'%(DATABASE_FILE), echo = False) 

Base = declarative_base()

##CLASSES##

class Gate(Base):
    __tablename__ = 'gate'
    id = Column(Integer, primary_key=True)
    secret = Column(String)
    location = Column(String)
    ##count =  Column(Integer) acho que já não é preciso
    def __repr__(self):
        return "<Gate(id=%d secret='%s', location='%s')>" % (
                                self.id, self.secret, self.location)
    def as_json(self):
        return {
            'id':self.id,
            'secret':self.secret,
            'location':self.location,
        }

class GateActivity(Base):
    __tablename__ = 'gateactivity'
    id= Column(Integer, primary_key=True)
    gate_id = Column(Integer)
    outcome = Column(String)
    time_stamp = Column(DateTime)
    ##count =  Column(Integer) acho que já não é preciso
    def __repr__(self):
        return "<Gate(id=%d secret='%s', location='%s')>" % (
            self.gate_id, self.outcome, self.time_stamp)
                
    def to_dictionary(self):
        return {
            'gate_id':self.gate_id,
            'outcome':self.outcome,
            'time_stamp':self.time_stamp,
        }
Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()


def newGate(ID,secret,location):
    gate = Gate(id = ID,secret = secret,location = location)
    session.add(gate)
    session.commit()


def newEvent(gateId,code,timeStamp):
    event = GateActivity(gate_id = gateId,outcome = code,time_stamp = timeStamp)
    session.add(event)
    session.commit()


def listGate():
    list = session.query(Gate).all()
    return [Gate.as_json(item) for item in list]

def getGateById(ID):
    resp = session.query(Gate).filter(Gate.id == ID).first()
    return resp

def Activity_list():
    ret_list = []
    lv = Activity()
    for v in lv:
        vd = v.to_dictionary()
        ret_list.append(vd)
    return ret_list

def Activity():
    return session.query(GateActivity).all()


