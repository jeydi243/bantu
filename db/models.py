from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, first_name='{self.first_name}', username='{self.username}')>"
