from database import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from sqlalchemy import select
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
import os 
from dotenv import load_dotenv

load_dotenv()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme= OAuth2PasswordBearer(tokenUrl ='/auth/login')

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    
    try:    
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        us_id = payload['user']
        result = await db.execute(select(User).where(User.id == us_id))
        user = result.scalar_one_or_none()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")