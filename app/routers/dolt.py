from fastapi import APIRouter, Depends

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Dict
from pydantic import Field

from database import get_db, engine
from database_schemas import Users, NotesDiffs

router = APIRouter(prefix="/dolt", tags=["dolt"])

@router.post("/commit")
async def dolt_commit(user_name : Annotated[str, (...)], db : AsyncSession = Depends(get_db)) -> Dict:
    res = await db.execute(select(Users).filter(Users.login == user_name))
    user = res.scalars().first()

    if user is  None:
        return {"data": "user not found"}

    async with engine.connect() as conn:
        await conn.execute(text("CALL DOLT_ADD('.');"))

        author = f"{user_name} <dolt@dolt.com>"
        message = f"commited by {user.login}"

        result = await conn.execute(
            text("CALL DOLT_COMMIT('--skip-empty', '--author', '"
                 + author
                 + "', '-m', '"
                 + message
                 + "')")
        )

    commit = None
    for row in result:
        commit = row[0]

    if not commit:
        return {"data": "Nothing to commit"}
    
    user.hash_previous_commit = commit

    db.add(user)          
    await db.commit()

    return {"data": f"Commit_hash: {commit}"}
    
@router.get("/previous_commit/{user_name}")
async def user_previous_commit(user_name : Annotated[str, Field(...)], db : AsyncSession = Depends(get_db)) -> Dict:
    res = await db.execute(
        select(Users)
        .filter(Users.login == user_name)
    )
    temp_user = res.scalars().first()

    if not temp_user:
        return {"data": f"User: {user_name} was not found"}

    res = await db.execute(
        select(NotesDiffs)
        .filter(NotesDiffs.to_commit ==temp_user.hash_previous_commit)
    )

    temp_diffs = res.scalars().first()

    if not temp_diffs:
        return {"data": f"Commit: {temp_user.hash_previous_commit} was not found"}
    
    return {"data": "Success",
            "to_title": temp_diffs.to_title,
            "to_text":  temp_diffs.to_text
    }

    