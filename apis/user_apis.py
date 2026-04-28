from models.user_model import User
import numpy as np
from sqlalchemy import select

async def create_user(db, email, embedding, name):
    user = User(
        name=name,
        email=email,
        embedding=embedding
    )
    db.add(user)
    await db.commit()
   
async def get_user(db, email):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()