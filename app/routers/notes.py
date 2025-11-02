from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import NoteBase, Note
from database_schemas import Users, Notes


router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/create")
async def create_note(note : NoteBase, db : AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Users).filter(Users.login == note.author_name))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(select(Users).filter(Users.login == note.author_name))
    temp_author_id = result.scalars().first()

    if (await db.execute(
        select(Notes).filter(Notes.author_id == temp_author_id.id))
    ).scalars().first():
        raise HTTPException(status_code=409, detail="You can have only one note")
    
    new_note = Notes(title = note.title, text = note.text, author_id = temp_author_id.id)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return {"data": "successfully created"}

        
@router.get("/show/{author_name}")
async def show_note_by_author_name(author_name : str, db : AsyncSession = Depends(get_db)) -> List:
    result = await db.execute(
        select(Users)
        .options(selectinload(Users.notes))
        .filter(Users.login == author_name)
    )
    temp_user = result.scalars().first()
    if not temp_user:
        raise HTTPException(status_code=404)
    return [{"title": note.title, "text": note.text} for note in temp_user.notes]