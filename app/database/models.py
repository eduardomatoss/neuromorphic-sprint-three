from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Example(Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)
