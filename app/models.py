from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,nullable=False,unique=True)
    password_hash = Column(String,nullable=False)
    appointments = relationship("Appointment")
class Appointment(Base):
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=True)
    description = Column(String,nullable=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    owner_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User")