from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import Optional

from database import Base

class Users(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    login : Mapped[str] = mapped_column(String(64), index=True)
    password : Mapped[str] = mapped_column(String(64))
    hash_previous_commit : Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    notes = relationship("Notes", back_populates="author")

class Notes(Base):
    __tablename__ = "notes"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title : Mapped[str] = mapped_column(String(64), index=True)
    text : Mapped[str] = mapped_column(String(64))
    author_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    author = relationship("Users", back_populates="notes")

class NotesDiffs(Base):
    __tablename__ = "dolt_diff_notes"

    to_commit: Mapped[Optional[str]] = mapped_column(String(1023), nullable=True, unique=True, primary_key=True)
    from_commit: Mapped[Optional[str]] = mapped_column(String(1023), nullable=True, unique=True, primary_key=True)

    to_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    to_title: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    to_text: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    to_author_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    to_commit_date: Mapped[Optional[str]] = mapped_column(DateTime, nullable=True)

    from_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    from_title: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    from_text: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    from_author_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    from_commit_date: Mapped[Optional[str]] = mapped_column(DateTime, nullable=True)

    diff_type: Mapped[Optional[str]] = mapped_column(String(1023), nullable=True)