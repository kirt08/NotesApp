from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(64), index=True)
    password = Column(String(64))

    notes = relationship("Notes", back_populates="author")

class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), index=True)
    text = Column(String(64))
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("Users", back_populates="notes")