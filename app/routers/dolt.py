from fastapi import APIRouter, Depends

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Dict

from database import get_db, engine
from database_schemas import Users

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
        if commit:
            return {"data": commit}
        else:
            return {"data": "Nothing to commit"}
    
