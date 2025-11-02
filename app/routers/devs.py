from fastapi import APIRouter, Depends
from typing import Dict, List, Annotated

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Note
from database_schemas import Users, Notes
from database import get_db, Base, engine

router = APIRouter(prefix="/devs", tags=["devs"])

@router.post("/reset_tables")
async def reset_tables(db: AsyncSession = Depends(get_db)) -> Dict:
    try:
        async with db.begin():
            await db.run_sync(lambda sync_session: Base.metadata.drop_all(sync_session.bind))
            await db.run_sync(lambda sync_session: Base.metadata.create_all(sync_session.bind))
        return {"data": True}
    except Exception as e:
        return {"data": False, "error": str(e)}

@router.get("/show_users")
async def show_users(N : Annotated[int, ()] = 10, db : AsyncSession = Depends(get_db)) -> List[User]:
    return (await db.execute(
        select(Users).limit(N)
    )).scalars().all()

@router.get("/show_notes")
async def show_notes(N : Annotated[int, ()] = 10, db : AsyncSession = Depends(get_db)) -> List[Note]:
    saved_notes = (await db.execute(
        select(Notes)
        .options(selectinload(Notes.author))
        .limit(N)
    )).scalars().all()
    answer_notes = [Note(title=saved_note.title, text=saved_note.text,
                         author_name=saved_note.author.login, id=saved_note.id) 
                    for saved_note in saved_notes]
    return answer_notes